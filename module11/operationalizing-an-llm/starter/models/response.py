"""
Model for LLM responses with metadata
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    """Model for LLM responses with metadata"""

    text: str
    model_used: str
    tokens_used: int
    latency_ms: float
    fallback_used: bool = False
    fallback_level: int = 0  # 0=no fallback, 1=alt model, 2=rule-based
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
