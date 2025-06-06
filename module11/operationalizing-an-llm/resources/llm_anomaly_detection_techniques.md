# LLM Anomaly Detection Techniques

## Introduction

Anomaly detection for Large Language Models (LLMs) is a critical component of production-ready AI systems. Unlike traditional software where errors are typically deterministic and clearly defined, LLMs can produce subtle, probabilistic anomalies that are challenging to detect. This document explores techniques for identifying unusual LLM behavior, implementing statistical detection methods, and establishing metrics that indicate potential issues.

## What Constitutes "Unusual" Behavior in LLMs?

LLM anomalies can manifest in various ways, often less obvious than traditional software failures. Understanding these patterns is the first step in building effective detection systems.

### Content-Based Anomalies

1. **Hallucinations**: When an LLM confidently presents incorrect information as fact
   - Example: Citing non-existent research papers or inventing statistics
   - Detection challenge: Requires factual verification against trusted sources

2. **Semantic Drift**: When responses gradually deviate from expected content areas
   - Example: A financial advisor LLM starting to discuss unrelated topics
   - Detection challenge: Requires understanding of domain boundaries

3. **Repetition Patterns**: Unusual repetition of phrases or circular reasoning
   - Example: "The solution is to solve the problem by finding a solution..."
   - Detection challenge: Distinguishing intentional repetition from anomalous loops

4. **Inconsistency**: Contradicting previous statements within the same conversation
   - Example: First stating a fact, then denying it later in the conversation
   - Detection challenge: Requires maintaining conversation state and logical analysis

5. **Prompt Leakage**: When system prompts or instructions appear in the output
   - Example: "As an AI assistant, I should respond professionally..." appearing in user-facing text
   - Detection challenge: Requires pattern matching against known system prompts

### Performance-Based Anomalies

1. **Latency Spikes**: Unusual processing time for certain types of requests
   - Example: A typically fast query suddenly taking 5x longer to process
   - Detection challenge: Distinguishing between model issues and infrastructure problems

2. **Token Usage Anomalies**: Unexpected patterns in token consumption
   - Example: Generating responses that are unusually long or short for similar queries
   - Detection challenge: Establishing appropriate baselines for different query types

3. **Error Rate Changes**: Sudden increases in specific types of errors
   - Example: A spike in "context length exceeded" errors for typical queries
   - Detection challenge: Distinguishing between model issues and input pattern changes

4. **Confidence Score Fluctuations**: Unusual patterns in model confidence
   - Example: Very high confidence scores for factually incorrect information
   - Detection challenge: Not all models expose confidence scores directly

### User Interaction Anomalies

1. **Feedback Pattern Changes**: Shifts in how users rate or interact with responses
   - Example: A sudden increase in negative feedback for a previously reliable query type
   - Detection challenge: Separating model issues from changes in user expectations

2. **Conversation Abandonment**: Users ending conversations prematurely
   - Example: Users consistently dropping off after specific types of responses
   - Detection challenge: Attributing abandonment to model issues versus other factors

3. **Repeated Queries**: Users asking the same question multiple times
   - Example: Reformulating questions suggests users aren't getting satisfactory answers
   - Detection challenge: Distinguishing clarification from dissatisfaction

## Statistical Methods for Anomaly Detection

Implementing effective anomaly detection requires appropriate statistical techniques that can identify unusual patterns while minimizing false positives.

### Baseline Establishment

Before detecting anomalies, you must establish what "normal" looks like for your specific LLM application:

```python
# Example: Establishing baseline metrics
def establish_baselines(historical_data, metric_names, window_size=1000):
    """Calculate baseline statistics for multiple metrics"""
    baselines = {}
    
    for metric in metric_names:
        # Extract the specific metric values
        values = [record[metric] for record in historical_data if metric in record]
        
        if not values:
            continue
            
        # Calculate basic statistics
        baselines[metric] = {
            "mean": np.mean(values),
            "median": np.median(values),
            "std_dev": np.std(values),
            "p5": np.percentile(values, 5),
            "p95": np.percentile(values, 95),
            # Store recent values for moving average
            "recent_values": collections.deque(maxlen=window_size)
        }
    
    return baselines
```

Effective baselines should account for:

- **Time-based patterns**: Daily, weekly, or seasonal variations
- **Query-type variations**: Different expectations for different types of requests
- **User segments**: Different usage patterns across user groups
- **Model versions**: Changes in behavior after model updates

### Z-Score Analysis

Z-scores measure how many standard deviations a data point is from the mean, making them useful for identifying outliers:

```python
def calculate_z_score(value, mean, std_dev):
    """Calculate z-score for a value"""
    # Avoid division by zero
    if std_dev == 0:
        return 0
    return (value - mean) / std_dev

def detect_anomalies_z_score(metrics, baselines, threshold=3.0):
    """Detect anomalies using z-score method"""
    anomalies = {}
    
    for metric, value in metrics.items():
        if metric in baselines:
            z_score = calculate_z_score(
                value, 
                baselines[metric]["mean"], 
                baselines[metric]["std_dev"]
            )
            
            if abs(z_score) > threshold:
                anomalies[metric] = {
                    "value": value,
                    "z_score": z_score,
                    "baseline_mean": baselines[metric]["mean"],
                    "baseline_std": baselines[metric]["std_dev"]
                }
    
    return anomalies
```

Z-scores work well for metrics with normal distributions but may need adjustments for metrics with skewed distributions.

### Moving Average Comparisons

Moving averages help detect shifts in behavior over time, which is particularly useful for identifying gradual drift:

```python
def detect_anomalies_moving_average(current_metrics, baselines, window_size=100, threshold=2.0):
    """Detect anomalies by comparing to recent moving averages"""
    anomalies = {}
    
    for metric, value in current_metrics.items():
        if metric in baselines:
            # Update recent values
            baselines[metric]["recent_values"].append(value)
            
            # Calculate moving average
            moving_avg = sum(baselines[metric]["recent_values"]) / len(baselines[metric]["recent_values"])
            
            # Calculate moving standard deviation
            moving_std = np.std(baselines[metric]["recent_values"])
            
            # Calculate deviation from moving average
            if moving_std > 0:
                deviation = abs(value - moving_avg) / moving_std
                
                if deviation > threshold:
                    anomalies[metric] = {
                        "value": value,
                        "moving_avg": moving_avg,
                        "deviation": deviation
                    }
    
    return anomalies
```

Moving averages are particularly effective for metrics that evolve naturally over time, such as token usage patterns as users become more familiar with the system.

### Multivariate Anomaly Detection

Many LLM anomalies manifest across multiple metrics simultaneously. Multivariate techniques can detect these complex patterns:

```python
def detect_multivariate_anomalies(metrics, correlation_matrix, threshold=0.8):
    """Detect anomalies based on unusual combinations of metrics"""
    anomalies = []
    
    # Check pairs of metrics that should be correlated
    for (metric1, metric2), expected_correlation in correlation_matrix.items():
        if metric1 in metrics and metric2 in metrics:
            # Calculate actual correlation
            actual_correlation = calculate_correlation(metrics[metric1], metrics[metric2])
            
            # Check if correlation differs significantly from expected
            if abs(actual_correlation - expected_correlation) > threshold:
                anomalies.append({
                    "metrics": [metric1, metric2],
                    "expected_correlation": expected_correlation,
                    "actual_correlation": actual_correlation,
                    "difference": abs(actual_correlation - expected_correlation)
                })
    
    return anomalies
```

Multivariate detection is particularly useful for identifying subtle anomalies that might not trigger thresholds on individual metrics but represent unusual combinations of values.

### Seasonal Decomposition

For LLM systems with cyclical usage patterns, seasonal decomposition helps separate expected variations from true anomalies:

```python
from statsmodels.tsa.seasonal import seasonal_decompose

def detect_seasonal_anomalies(time_series, period=24, threshold=3.0):
    """Detect anomalies accounting for seasonal patterns"""
    # Decompose time series into trend, seasonal, and residual components
    decomposition = seasonal_decompose(time_series, period=period)
    
    # Extract residuals (what remains after removing trend and seasonality)
    residuals = decomposition.resid
    
    # Calculate standard deviation of residuals
    residual_std = np.std(residuals[~np.isnan(residuals)])
    
    # Identify points where residuals exceed threshold
    anomalies = []
    for i, residual in enumerate(residuals):
        if not np.isnan(residual) and abs(residual) > threshold * residual_std:
            anomalies.append({
                "index": i,
                "original_value": time_series[i],
                "residual": residual,
                "threshold": threshold * residual_std
            })
    
    return anomalies
```

This approach is valuable for systems with daily, weekly, or monthly usage patterns, as it can distinguish between expected cyclical variations and true anomalies.

## Key Metrics for LLM Monitoring

Effective anomaly detection requires tracking the right metrics. Here are key indicators to monitor for LLM systems:

### Response Content Metrics

1. **Perplexity**: Measures how "surprised" the model is by the text it generates
   - Higher values can indicate the model is generating unusual content
   - Calculation: Based on the negative log likelihood of generated tokens

2. **Toxicity Scores**: Measures potentially harmful content
   - Sudden increases may indicate prompt injection or model misuse
   - Implementation: Often requires specialized content moderation models

3. **Topic Coherence**: Measures how well the response stays on topic
   - Decreases can indicate semantic drift or hallucinations
   - Implementation: Embedding similarity between prompt and response

4. **Factual Consistency**: Measures alignment with known facts
   - Decreases can indicate hallucinations or reasoning errors
   - Implementation: Requires knowledge base verification or specialized fact-checking models

### Performance Metrics

1. **Token Counts**: Input and output token usage
   - Unusual patterns can indicate inefficient prompting or model issues
   - Tracking: Monitor by request type and user segment

2. **Latency Breakdown**:
   - Prompt processing time
   - Model inference time
   - Post-processing time
   - Unusual ratios between these components can indicate specific issues

3. **Error Rates by Category**:
   - Rate limiting errors
   - Context length errors
   - Content policy violations
   - Authentication failures
   - Spikes in specific error types often indicate systemic issues

4. **Cache Hit Rates**: For systems implementing response caching
   - Sudden drops can indicate changing query patterns or cache invalidation issues
   - Tracking: Monitor by query type and time period

### User Interaction Metrics

1. **User Feedback Scores**: Explicit ratings or feedback
   - Decreases can indicate degrading model performance
   - Tracking: Monitor by query type, user segment, and model version

2. **Conversation Length**: Number of turns in a conversation
   - Shorter conversations might indicate user frustration
   - Longer conversations might indicate the model is not being helpful

3. **Query Reformulation Rate**: How often users rephrase their questions
   - Increases can indicate the model is not understanding or answering correctly
   - Implementation: Requires semantic similarity analysis between consecutive queries

4. **Feature Usage Patterns**: Which model capabilities are being used
   - Changes can indicate shifting user needs or problems with specific features
   - Tracking: Monitor by user segment and time period

## Implementation Techniques

Translating these concepts into a practical anomaly detection system requires thoughtful implementation:

### Real-Time vs. Batch Detection

Different anomalies require different detection approaches:

1. **Real-Time Detection**: For immediate action on critical issues
   - Implemented during request processing
   - Focuses on per-request metrics and simple statistical tests
   - Example: Detecting toxic content or extremely long responses

2. **Batch Detection**: For identifying patterns across multiple requests
   - Implemented as scheduled jobs (hourly, daily)
   - Focuses on aggregate metrics and more complex statistical analysis
   - Example: Detecting gradual drift in response quality or user satisfaction

### Anomaly Scoring System

A practical approach is to implement a composite anomaly score that combines multiple signals:

```python
def calculate_anomaly_score(metrics, baselines, weights=None):
    """Calculate a composite anomaly score from multiple metrics"""
    if weights is None:
        # Default equal weighting
        weights = {metric: 1.0 for metric in metrics}
    
    total_score = 0.0
    total_weight = 0.0
    
    for metric, value in metrics.items():
        if metric in baselines and metric in weights:
            # Calculate z-score for this metric
            z_score = calculate_z_score(
                value,
                baselines[metric]["mean"],
                baselines[metric]["std_dev"]
            )
            
            # Add to weighted score
            total_score += abs(z_score) * weights[metric]
            total_weight += weights[metric]
    
    # Normalize score to 0-1 range
    if total_weight > 0:
        normalized_score = total_score / (total_weight * 5)  # Assuming z-scores rarely exceed 5
        return min(normalized_score, 1.0)  # Cap at 1.0
    
    return 0.0
```

This approach allows for:
- Prioritizing certain metrics over others
- Combining different types of anomalies into a single actionable score
- Setting appropriate thresholds for alerts and interventions

### Contextual Anomaly Detection

Context matters significantly in LLM anomaly detection. What's normal for one type of query may be anomalous for another:

```python
def detect_contextual_anomalies(metrics, query_type, user_segment, baselines):
    """Detect anomalies considering the specific context"""
    # Get the appropriate baseline for this context
    context_key = f"{query_type}_{user_segment}"
    
    if context_key in baselines:
        context_baseline = baselines[context_key]
    else:
        # Fall back to general baseline if specific context not available
        context_baseline = baselines.get("general", {})
    
    # Detect anomalies using context-specific baselines
    anomalies = {}
    for metric, value in metrics.items():
        if metric in context_baseline:
            z_score = calculate_z_score(
                value,
                context_baseline[metric]["mean"],
                context_baseline[metric]["std_dev"]
            )
            
            # Use context-appropriate thresholds
            threshold = context_baseline.get("thresholds", {}).get(metric, 3.0)
            
            if abs(z_score) > threshold:
                anomalies[metric] = {
                    "value": value,
                    "z_score": z_score,
                    "context": context_key
                }
    
    return anomalies
```

Implementing contextual detection requires:
- Classifying requests into meaningful categories
- Maintaining separate baselines for different contexts
- Adjusting thresholds based on context-specific expectations

### Anomaly Response Actions

Once anomalies are detected, the system should take appropriate actions:

1. **Logging and Alerting**:
   - Record detailed information about the anomaly
   - Trigger alerts for human review of critical issues

2. **Automatic Remediation**:
   - Activate fallback mechanisms for severe anomalies
   - Adjust request parameters to mitigate issues

3. **Feedback Collection**:
   - Flag anomalous interactions for targeted user feedback
   - Gather additional context to improve detection

4. **Model Monitoring**:
   - Track anomaly patterns to identify potential model degradation
   - Inform model retraining or fine-tuning decisions

## Integration with LLM Middleware

Anomaly detection should be integrated throughout the LLM middleware architecture:

```python
# Example integration with middleware
class AnomalyDetectionMiddleware:
    def __init__(self, config):
        self.config = config
        self.baselines = load_baselines(config.baseline_path)
        self.anomaly_detector = AnomalyDetector(self.baselines)
        self.logger = setup_logger(config.logging)
        
    async def process(self, request, context, next_middleware):
        """Process a request with anomaly detection"""
        # Pre-processing anomaly checks (input validation)
        input_metrics = extract_input_metrics(request)
        input_anomalies = self.anomaly_detector.detect(input_metrics)
        
        if self.should_block_request(input_anomalies):
            return create_error_response("Request blocked due to anomalous input")
        
        # Process the request
        start_time = time.time()
        response = await next_middleware(request, context)
        processing_time = time.time() - start_time
        
        # Post-processing anomaly checks
        output_metrics = extract_output_metrics(response, processing_time)
        output_anomalies = self.anomaly_detector.detect(output_metrics)
        
        # Record all metrics and anomalies
        self.record_metrics(request, response, input_metrics, output_metrics)
        
        if input_anomalies or output_anomalies:
            self.logger.warning(
                "Anomalies detected",
                extra={
                    "request_id": context.request_id,
                    "input_anomalies": input_anomalies,
                    "output_anomalies": output_anomalies
                }
            )
            
            # Take appropriate actions based on anomaly severity
            self.handle_anomalies(input_anomalies, output_anomalies, response)
        
        return response
```

This middleware approach allows anomaly detection to be:
- Applied consistently across all requests
- Integrated with logging and monitoring systems
- Configured with appropriate thresholds and actions

For more details on the overall middleware architecture, see the [LLM Middleware Architecture Overview](llm_middleware_architecture_overview.md).

## Practical Implementation Example

Let's examine a complete example of implementing anomaly detection for an LLM-powered customer support system:

### 1. Define Metrics to Monitor

```python
# Key metrics for customer support LLM
METRICS = {
    # Content metrics
    "response_length": {"weight": 1.0, "threshold": 2.5},
    "topic_relevance_score": {"weight": 1.5, "threshold": 2.0},
    "sentiment_score": {"weight": 0.8, "threshold": 3.0},
    
    # Performance metrics
    "latency_ms": {"weight": 1.0, "threshold": 3.0},
    "token_count_input": {"weight": 0.7, "threshold": 3.0},
    "token_count_output": {"weight": 0.7, "threshold": 2.5},
    
    # User interaction metrics
    "user_feedback_score": {"weight": 2.0, "threshold": 2.0},
    "follow_up_questions": {"weight": 1.2, "threshold": 2.5}
}
```

### 2. Implement Metric Collection

```python
def collect_metrics(request, response, user_feedback=None):
    """Collect all relevant metrics for anomaly detection"""
    metrics = {
        # Content metrics
        "response_length": len(response.text),
        "topic_relevance_score": calculate_topic_relevance(request.prompt, response.text),
        "sentiment_score": analyze_sentiment(response.text),
        
        # Performance metrics
        "latency_ms": response.completion_time - request.start_time,
        "token_count_input": count_tokens(request.prompt),
        "token_count_output": count_tokens(response.text),
    }
    
    # Add user feedback if available
    if user_feedback:
        metrics["user_feedback_score"] = user_feedback.score
        metrics["follow_up_questions"] = user_feedback.follow_up_count
    
    return metrics
```

### 3. Implement Detection Logic

```python
class AnomalyDetector:
    def __init__(self, config):
        self.config = config
        self.baselines = load_baselines()
        self.metrics_store = MetricsStore()
        
    def detect_anomalies(self, metrics, context=None):
        """Detect anomalies in the provided metrics"""
        anomalies = {}
        context_key = context or "general"
        
        # Get appropriate baselines
        baseline = self.baselines.get(context_key, self.baselines.get("general", {}))
        
        # Check each metric
        for metric_name, value in metrics.items():
            if metric_name in baseline and metric_name in self.config.metrics:
                # Get configuration for this metric
                metric_config = self.config.metrics[metric_name]
                threshold = metric_config.get("threshold", 3.0)
                
                # Calculate z-score
                z_score = (value - baseline[metric_name]["mean"]) / baseline[metric_name]["std_dev"]
                
                # Check if it exceeds threshold
                if abs(z_score) > threshold:
                    anomalies[metric_name] = {
                        "value": value,
                        "expected": baseline[metric_name]["mean"],
                        "z_score": z_score,
                        "threshold": threshold
                    }
        
        # Calculate overall anomaly score
        anomaly_score = self.calculate_anomaly_score(metrics, anomalies)
        
        return {
            "anomalies": anomalies,
            "score": anomaly_score,
            "is_anomalous": anomaly_score > self.config.anomaly_threshold
        }
    
    def calculate_anomaly_score(self, metrics, detected_anomalies):
        """Calculate overall anomaly score"""
        if not detected_anomalies:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric_name, anomaly in detected_anomalies.items():
            weight = self.config.metrics.get(metric_name, {}).get("weight", 1.0)
            total_score += abs(anomaly["z_score"]) * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        # Normalize to 0-1 range
        normalized_score = min(total_score / (total_weight * 5), 1.0)
        return normalized_score
```

### 4. Implement Response Actions

```python
def handle_anomalies(anomaly_result, request, response):
    """Take appropriate actions based on detected anomalies"""
    if not anomaly_result["is_anomalous"]:
        return
    
    # Log the anomaly
    logger.warning(
        f"Anomaly detected (score: {anomaly_result['score']:.2f})",
        extra={
            "request_id": request.id,
            "anomalies": anomaly_result["anomalies"],
            "score": anomaly_result["score"]
        }
    )
    
    # Determine severity
    if anomaly_result["score"] > 0.8:
        severity = "critical"
    elif anomaly_result["score"] > 0.5:
        severity = "high"
    else:
        severity = "medium"
    
    # Take action based on severity
    if severity == "critical":
        # For critical anomalies, use fallback and alert
        alert_team(anomaly_result, request, response)
        return generate_fallback_response(request)
    
    elif severity == "high":
        # For high severity, flag for review but still return
        flag_for_review(anomaly_result, request, response)
        
    # Record for analytics
    record_anomaly_for_analysis(anomaly_result, request, response)
    
    # Return original response with warning if appropriate
    return response
```

### 5. Update Baselines Periodically

```python
def update_baselines(metrics_store, config):
    """Periodically update baselines with recent data"""
    # Get recent metrics
    recent_metrics = metrics_store.get_recent_metrics(days=7)
    
    # Group by context
    grouped_metrics = {}
    for record in recent_metrics:
        context = record.get("context", "general")
        if context not in grouped_metrics:
            grouped_metrics[context] = {}
            
        # Group metrics by name
        for metric_name, value in record["metrics"].items():
            if metric_name not in grouped_metrics[context]:
                grouped_metrics[context][metric_name] = []
            
            grouped_metrics[context][metric_name].append(value)
    
    # Calculate new baselines
    new_baselines = {}
    for context, metrics in grouped_metrics.items():
        new_baselines[context] = {}
        
        for metric_name, values in metrics.items():
            if len(values) >= config.min_samples_for_baseline:
                new_baselines[context][metric_name] = {
                    "mean": np.mean(values),
                    "median": np.median(values),
                    "std_dev": np.std(values),
                    "p5": np.percentile(values, 5),
                    "p95": np.percentile(values, 95),
                    "updated_at": datetime.now().isoformat()
                }
    
    # Save new baselines
    save_baselines(new_baselines)
    
    return new_baselines
```

## Conclusion

Effective anomaly detection is essential for operating reliable LLM systems in production. By understanding what constitutes unusual behavior, implementing appropriate statistical methods, and tracking key metrics, you can identify and address issues before they significantly impact users.

The techniques described in this document should be adapted to your specific use case, considering the unique characteristics of your LLM application, user base, and operational requirements. Remember that anomaly detection is not a one-time setup but an ongoing process that requires continuous refinement as your system evolves.

For more information on implementing these techniques within a complete middleware architecture, see the [LLM Middleware Architecture Overview](llm_middleware_architecture_overview.md). For details on implementing fallback mechanisms when anomalies are detected, refer to the [Tiered Fallback Mechanisms Guide](tiered_fallback_mechanisms_guide.md).

## References

- Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly detection: A survey. ACM Computing Surveys.
- Hendrycks, D., & Gimpel, K. (2016). A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks.
- Ren, J., et al. (2019). Likelihood Ratios for Out-of-Distribution Detection.
- Google Cloud. (2023). Best practices for LLM application monitoring.
