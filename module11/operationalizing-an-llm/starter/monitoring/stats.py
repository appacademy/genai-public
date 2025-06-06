"""
Usage statistics tracking for LLM requests
"""

import logging
import statistics
from typing import Dict, Any, List
from datetime import datetime

from models.request import LLMRequest
from models.response import LLMResponse
from models.metrics import PerformanceMetrics
from utils.text_utils import sanitize_text


class StatsTracker:
    """Class for tracking and analyzing LLM usage statistics"""

    def __init__(self, max_recent_requests: int = 50):
        self.logger = logging.getLogger("llm_app")
        self.recent_requests: List[Dict[str, Any]] = []
        self.max_recent_requests = max_recent_requests

    def store_request(
        self, request: LLMRequest, response: LLMResponse, metrics: PerformanceMetrics
    ) -> None:
        """Store recent request data for analysis"""
        request_data = {
            "request_id": request.request_id,
            "timestamp": datetime.now().isoformat(),
            "prompt": sanitize_text(request.prompt),
            "response": (
                response.text[:100] + "..."
                if len(response.text) > 100
                else response.text
            ),
            "model": response.model_used,
            "fallback_level": response.fallback_level,
            "latency_ms": response.latency_ms,
            "tokens": response.tokens_used,
            "anomaly_score": metrics.anomaly_score,
        }

        self.recent_requests.append(request_data)

        # Keep only the most recent requests
        if len(self.recent_requests) > self.max_recent_requests:
            self.recent_requests.pop(0)

    def get_recent_performance(self) -> Dict[str, Any]:
        """Get performance statistics from recent requests"""
        if not self.recent_requests:
            return {"error": "No requests recorded yet"}

        try:
            # Calculate statistics
            latencies = [r["latency_ms"] for r in self.recent_requests]
            tokens = [r["tokens"] for r in self.recent_requests]
            fallbacks = sum(1 for r in self.recent_requests if r["fallback_level"] > 0)

            stats = {
                "request_count": len(self.recent_requests),
                "avg_latency_ms": statistics.mean(latencies),
                "max_latency_ms": max(latencies),
                "min_latency_ms": min(latencies),
                "avg_tokens": statistics.mean(tokens),
                "total_tokens": sum(tokens),
                "fallback_rate": (
                    fallbacks / len(self.recent_requests) if self.recent_requests else 0
                ),
                "high_anomaly_count": sum(
                    1 for r in self.recent_requests if r.get("anomaly_score", 0) > 0.7
                ),
            }

            return stats
        except Exception as e:
            self.logger.error(f"Error calculating performance stats: {str(e)}")
            return {"error": str(e)}

    def get_model_usage_stats(self) -> Dict[str, Any]:
        """Get statistics about which models are being used"""
        if not self.recent_requests:
            return {"error": "No requests recorded yet"}

        try:
            # Extract model usage information
            models_used = [r["model"] for r in self.recent_requests]
            model_counts = {
                model: models_used.count(model) for model in set(models_used)
            }

            # Calculate fallback levels
            fallback_levels = [r["fallback_level"] for r in self.recent_requests]
            level_counts = {
                "primary": fallback_levels.count(0),
                "first_fallback": fallback_levels.count(1),
                "second_fallback": fallback_levels.count(2),
                "rule_based": sum(
                    1
                    for r in self.recent_requests
                    if r["model"] == "rule_based_fallback"
                ),
            }

            return {
                "total_requests": len(models_used),
                "model_usage": model_counts,
                "model_usage_percent": {
                    m: round((c / len(models_used)) * 100, 2)
                    for m, c in model_counts.items()
                },
                "fallback_levels": level_counts,
                "fallback_levels_percent": {
                    k: round((v / len(fallback_levels)) * 100, 2)
                    for k, v in level_counts.items()
                },
            }
        except Exception as e:
            self.logger.error(f"Error calculating model usage stats: {str(e)}")
            return {"error": str(e)}
