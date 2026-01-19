# Ubuntu System Repair Agent

Autonomous multi-agent system for diagnosing and repairing Ubuntu server issues using LangGraph, MCP protocol, and local LLMs.

## Problem

System administrators spend hours manually diagnosing and fixing repetitive server issues. This agent automates that process with intelligent diagnosis, solution generation, and safe execution.

## Architecture

### Multi-Agent Design with MCP
```
┌─────────────────────────────────────┐
│        Detector Agent               │
│  ┌─────────────────────────────┐   │
│  │   MCP Server (Detector)     │   │
│  │   - check_service_status    │   │
│  │   - check_disk_usage        │   │
│  │   - read_logs               │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Fixer Agent                 │
│  ┌─────────────────────────────┐   │
│  │   MCP Server (Fixer)        │   │
│  │   - search_ubuntu_docs      │   │
│  │   - generate_alternatives   │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        Executor Agent               │
│  ┌─────────────────────────────┐   │
│  │   MCP Server (Executor)     │   │
│  │   - validate_command_safety │   │
│  │   - execute_bash_command    │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼ (if failure)
   Smart Retry Logic:
   - Failures 1-2: Try alternative solutions (→ Fixer)
   - Failure 3: Re-diagnose issue (→ Detector)
   - Failure 5: Escalate to human
```

## Tech Stack

- **LangGraph**: Agent orchestration and workflow
- **MCP (Model Context Protocol)**: Standardized tool layer
- **Ollama**: Local LLM hosting
- **Python**: Agent logic and MCP servers

## Project Structure
```
ubuntu-repair-agent/
├── src/
│   ├── agents/
│   │   ├── detector/
│   │   │   ├── __init__.py       # Exports
│   │   │   ├── agent.py          # Detector logic + MCP client
│   │   │   ├── mcp_server.py     # System diagnostic tools
│   │   │   ├── prompts.py        # Detector prompts
│   │   │   ├── schemas.py        # Response models
│   │   │   └── test.py           # Standalone test script
│   │   ├── fixer/
│   │   │   ├── agent.py          # Fixer logic (TODO)
│   │   │   ├── prompts.py        # Fixer prompts
│   │   │   └── mcp_server.py     # Documentation search tools
│   │   └── executor/
│   │       ├── agent.py          # Executor logic (TODO)
│   │       ├── prompts.py        # Executor prompts
│   │       └── mcp_server.py     # Command execution tools
│   ├── config.py                 # LLM configuration (Ollama)
│   ├── state.py                  # Shared state definition
│   └── graph.py                  # LangGraph workflow (TODO)
├── main.py                       # Entry point
└── README.md
```

## Current Status

**Completed:**
- ✅ Detector Agent with MCP integration
- ✅ Three diagnostic tools (disk usage, logs, service status)
- ✅ Structured output with Pydantic models
- ✅ Standalone testing capability

**In Progress:**
- 🚧 Fixer Agent implementation
- 🚧 Executor Agent implementation
- 🚧 LangGraph workflow integration

**Next Steps:**
- Build Fixer and Executor agents
- Create LangGraph workflow with smart retry logic
- Add human-in-the-loop for risky commands

## Contributing

**Areas we need help:**

1. **MCP Server Development**: Build tool servers for system diagnostics, command execution
2. **Agent Design**: Improve routing logic and retry strategies  
3. **Testing**: Run on different Ubuntu configurations
4. **Documentation**: Architecture diagrams, tutorials


## Installation
```bash
# Clone repo
git clone https://github.com/knightscode139/ubuntu-repair-agent.git
cd ubuntu-repair-agent

# Install dependencies
uv sync

# Ensure Ollama is running with a compatible model
ollama pull llama3.1:8b
```

## Testing

### Test Detector Agent
```bash
uv run python src/agents/detector/test.py
```

Example interaction:
```
👉 Enter system issue to diagnose: disk is full
🔍 Analyzing system...
📊 Diagnosis Result: [storage] Disk usage at 98%: The /var partition is full...
```

## Open Questions

1. Best LLM for tool calling reliability? (Llama 3.1 vs Qwen vs Mistral)
2. How to handle sudo-required commands safely?
3. Should we support multiple LLM providers or stick with Ollama?

## License

MIT

## Contact

- GitHub Issues for bugs, features, and discussions

---

**Note:** This is an active open-source project. Architecture decisions are made collaboratively with contributors.