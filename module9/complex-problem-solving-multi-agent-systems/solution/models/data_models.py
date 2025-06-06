from typing import Dict, Any
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    content: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Add additional shared data models for LangGraph state
class ProblemSolvingState(BaseModel):
    problem: str
    research_results: str = ""
    analysis_results: str = ""
    solution: str = ""
    critique: str = ""
    recommendation: str = "Revise"
    iteration: int = 1
    final_solution: str = ""
