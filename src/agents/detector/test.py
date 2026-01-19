import asyncio
import sys
import os

# Add src path to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
package_root = os.path.abspath(os.path.join(current_dir, '../../../'))
if package_root not in sys.path:
    sys.path.insert(0, package_root)

from src.agents.detector.agent import get_mcp_client, build_detector_agent


async def run_test():
    """Test the Detector Agent with terminal input."""
    print("🧪 Testing Detector Agent...")
    print("=" * 50)

    # Get MCP client and tools
    client = get_mcp_client()
    tools = await client.get_tools()

    print(f"✅ Loaded {len(tools)} tools from MCP server")
    for tool in tools:
        print(f"   - {tool.name}")

    # Create agent
    agent = build_detector_agent(tools)
    print("✅ Agent created successfully\n")

    # Get user input
    query = input("👉 Enter system issue to diagnose: ")

    print("\n🔍 Analyzing system...")
    print("=" * 50)

    # Invoke agent
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    # Display result
    print("\n📊 Diagnosis Result:")
    print("=" * 50)

    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        if hasattr(last_message, "content"):
            print(last_message.content)
        else:
            print(str(last_message))

        # Check for structured output
        if hasattr(last_message, "response_metadata") and "structured_output" in last_message.response_metadata:
            print("\n📋 Structured Output:")
            print(last_message.response_metadata["structured_output"])
    else:
        print("❌ No response from agent")


if __name__ == "__main__":
    try:
        asyncio.run(run_test())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
