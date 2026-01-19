from typing import Literal, Optional
from pydantic import BaseModel, Field

IssueCategory = Literal[
    "package_manager",
    "network",
    "storage",
    "system_service",
    "permission",
    "unknown"
]

DetectionStatus = Literal[
    "definitive_diagnosis",
    "needs_investigation",
    "critical_risk"
]

class DetectorResponse(BaseModel):
    """Call this tool when you have completed your diagnosis to provide the final answer."""
    status: DetectionStatus = Field(..., description="The current state of the diagnosis process.")
    category: IssueCategory = Field(..., description="The classified category of the system issue.")
    root_cause: Optional[str] = Field(None, description="The identified root cause. Only if status is definitive.")
    explanation: str = Field(..., description="Technical explanation of the findings.")
