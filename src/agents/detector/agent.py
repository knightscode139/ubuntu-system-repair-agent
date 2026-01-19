import asyncio
import os
from typing import Any, Dict, List
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool

from src.config import get_llm
from src.state import AgentState
from .schemas import DetectorResponse
from .prompts import SYSTEM_PROMPT


def get_mcp_client() -> MultiServerMCPClient:
    """
    Create and configure the MCP client for detector tools.

    Returns:
        Configured MultiServerMCPClient
    """
    # Get the path to the detector MCP server
    detector_server_path = os.path.join(
        os.path.dirname(__file__), "mcp_server.py"
    )

    client = MultiServerMCPClient({
        "detector": {
            "transport": "stdio",
            "command": "python",
            "args": [detector_server_path],
        }
    })

    return client


def build_detector_agent(tools: List[BaseTool]):
    """
    Build the Detector Agent with provided tools.

    Args:
        tools: List of LangChain tools (from MCP)

    Returns:
        Compiled agent graph
    """
    llm = get_llm()

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        response_format=DetectorResponse
    )

    return agent


async def create_detector_agent():
    """
    Creates the Detector Agent that diagnoses system issues.

    Returns:
        Compiled agent graph configured for detection tasks
    """
    # Get MCP tools from the server
    client = get_mcp_client()
    mcp_tools = await client.get_tools()

    # Build agent with tools
    agent = build_detector_agent(mcp_tools)

    return agent


async def detector_node_async(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node function for the Detector Agent (async).

    Args:
        state: Current agent state with user issue description

    Returns:
        Updated state with detection results
    """
    # Create agent with MCP tools
    agent = await create_detector_agent()

    # Prepare input - create_agent expects messages format
    user_input = state.get("issue", "Analyze the system for issues")

    # Invoke the agent with messages format
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )

    # Parse the response from the agent state
    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        # Check if the last message contains structured output
        if hasattr(last_message, "response_metadata") and "structured_output" in last_message.response_metadata:
            detector_response = last_message.response_metadata["structured_output"]
            issue_description = f"[{detector_response.category}] {detector_response.root_cause or 'Under investigation'}: {detector_response.explanation}"
        else:
            issue_description = last_message.content if hasattr(last_message, "content") else str(last_message)
    else:
        issue_description = "No diagnosis completed"

    return {
        "issue": issue_description,
        "retry_count": state.get("retry_count", 0)
    }


def detector_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node function for the Detector Agent (sync wrapper).

    Args:
        state: Current agent state with user issue description

    Returns:
        Updated state with detection results
    """
    return asyncio.run(detector_node_async(state))
