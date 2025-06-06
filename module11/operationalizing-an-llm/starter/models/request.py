"""
Model for LLM requests with validation
"""

import uuid
from pydantic import BaseModel, Field, validator


class LLMRequest(BaseModel):
    """Model for LLM requests with validation"""

    prompt: str
    max_tokens: int = Field(default=100, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0, le=2.0)
    model: str = "gemma3:4b"
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # Test flags as regular fields
    test_force_first_fallback_fail: bool = Field(default=False)
    test_force_all_models_fail: bool = Field(default=False)
    simulate_high_load: bool = Field(default=False)

    @validator("prompt")
    def prompt_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v
