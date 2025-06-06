"""
Performance monitoring for LLM requests
"""

import logging
from models.request import LLMRequest
from models.response import LLMResponse
from models.metrics import PerformanceMetrics
from monitoring.anomaly import detect_anomalies, update_metrics_history


def calculate_token_cost(
    model: str, prompt_tokens: int, completion_tokens: int
) -> float:
    """Calculate estimated cost of tokens used"""
    # For Ollama models, there is no direct cost since they run locally
    # This is a placeholder for compatibility - all costs are 0
    return 0.0


def monitor_performance(
    request: LLMRequest, response: LLMResponse
) -> PerformanceMetrics:
    """
    Implement performance monitoring

    Track metrics such as:
    - Response times
    - Token usage and cost
    - Anomaly detection (unusual responses)
    """
    logger = logging.getLogger("llm_app")

    # Create performance metrics object
    metrics = PerformanceMetrics(
        request_id=request.request_id,
        prompt_tokens=response.tokens_used
        // 2,  # Rough estimate, would be more accurate from API response
        completion_tokens=response.tokens_used // 2,  # Rough estimate
        total_tokens=response.tokens_used,
        latency_ms=response.latency_ms,
        model=response.model_used,
    )

    # Calculate cost if using a real model (not fallback)
    if response.fallback_level < 2:  # Not using rule-based fallback
        metrics.estimated_cost = calculate_token_cost(
            response.model_used, metrics.prompt_tokens, metrics.completion_tokens
        )

    # Update recent metrics for anomaly detection
    update_metrics_history(response.latency_ms, response.tokens_used)

    # Detect anomalies
    metrics.anomaly_score = detect_anomalies(metrics)

    # Log performance information
    log_level = logging.INFO
    if metrics.anomaly_score > 0.7:
        log_level = logging.WARNING

    logger.log(
        log_level,
        f"Performance: model={response.model_used}, "
        f"tokens={response.tokens_used}, latency={response.latency_ms:.2f}ms, "
        f"cost=${metrics.estimated_cost:.6f}, anomaly_score={metrics.anomaly_score:.2f}",
        extra={"request_id": request.request_id},
    )

    # Alert on high anomaly scores
    if metrics.anomaly_score > 0.7:
        logger.warning(
            f"ANOMALY DETECTED: Unusual performance characteristics "
            f"for request {request.request_id}",
            extra={"request_id": request.request_id},
        )

    return metrics
