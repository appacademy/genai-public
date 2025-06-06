"""
Model for tracking performance metrics
"""

from pydantic import BaseModel


class PerformanceMetrics(BaseModel):
    """Model for tracking performance metrics"""

    request_id: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: float
    model: str
    estimated_cost: float = 0.0
    anomaly_score: float = 0.0
