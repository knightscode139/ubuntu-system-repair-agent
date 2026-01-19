from typing import TypedDict

class AgentState(TypedDict):
    """Shared state passed between agents"""
    issue: str          # What problem was detected (None if system is healthy)
    solution: str       # What fix was suggested  
    result: str         # Execution result (SUCCESS/FAILED)
    retry_count: int    # Number of retry attempts
