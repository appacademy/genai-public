"""
Anomaly detection for performance metrics
"""

import statistics
from models.metrics import PerformanceMetrics

# Dictionary to store recent performance metrics for anomaly detection
recent_metrics = {
    "latencies": [],
    "token_counts": [],
    "max_metrics": 100,  # Keep last 100 requests for baseline
}


def detect_anomalies(metrics: PerformanceMetrics) -> float:
    """
    Detect anomalies in performance metrics
    Returns an anomaly score (0-1 where higher means more anomalous)
    """
    # Skip anomaly detection if we don't have enough baseline data
    if len(recent_metrics["latencies"]) < 5:
        return 0.0

    anomaly_score = 0.0

    # Check latency against recent history
    avg_latency = statistics.mean(recent_metrics["latencies"])
    std_latency = (
        statistics.stdev(recent_metrics["latencies"])
        if len(recent_metrics["latencies"]) > 1
        else avg_latency / 2
    )

    if metrics.latency_ms > avg_latency + 3 * std_latency:
        # More than 3 standard deviations above mean is highly anomalous
        anomaly_score += 0.5
    elif metrics.latency_ms > avg_latency + 2 * std_latency:
        # 2-3 standard deviations is moderately anomalous
        anomaly_score += 0.3

    # Check token count against recent history
    avg_tokens = statistics.mean(recent_metrics["token_counts"])
    std_tokens = (
        statistics.stdev(recent_metrics["token_counts"])
        if len(recent_metrics["token_counts"]) > 1
        else avg_tokens / 2
    )

    if metrics.total_tokens > avg_tokens + 3 * std_tokens:
        # Unusually high token usage
        anomaly_score += 0.5
    elif (
        metrics.total_tokens < avg_tokens - 2 * std_tokens and metrics.total_tokens > 0
    ):
        # Unusually low token usage (possible truncation issues)
        anomaly_score += 0.3

    return min(anomaly_score, 1.0)  # Cap at 1.0


def update_metrics_history(latency_ms: float, token_count: int) -> None:
    """Update the metrics history for anomaly detection"""
    recent_metrics["latencies"].append(latency_ms)
    recent_metrics["token_counts"].append(token_count)

    # Keep only the most recent metrics
    if len(recent_metrics["latencies"]) > recent_metrics["max_metrics"]:
        recent_metrics["latencies"].pop(0)
    if len(recent_metrics["token_counts"]) > recent_metrics["max_metrics"]:
        recent_metrics["token_counts"].pop(0)
