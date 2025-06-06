# Tiered Fallback Mechanisms for LLM Applications

## Introduction

In production LLM applications, failures are inevitable. External services experience outages, models encounter errors, and unexpected inputs can cause processing issues. A robust fallback strategy ensures your application remains functional and provides value to users even when components fail. This document provides step-by-step guidance for implementing tiered fallback mechanisms that gracefully degrade functionality while maintaining a coherent user experience.

## Understanding the Fallback Hierarchy

A well-designed fallback system follows a tiered approach, with each tier representing a different level of capability and reliability. As failures occur, the system cascades through these tiers, attempting to provide the best possible service given the available resources.

### Tier 1: Primary Model Strategy

The primary model represents your preferred LLM configuration, offering the highest quality responses and most advanced capabilities. This tier typically features:

- Larger, more capable models (e.g., GPT-4, Claude 3 Opus, Gemma 3 7B)
- Full parameter sets for optimal performance
- Complete access to tools and external data sources
- Maximum context window utilization

While this tier provides the best experience, it's also the most vulnerable to failures due to its complexity and external dependencies.

### Tier 2: Secondary Model Strategy

When the primary model fails, the system falls back to a secondary model that balances capability and reliability:

- Medium-sized models with good performance (e.g., GPT-3.5, Claude 3 Sonnet, Gemma 3 2B)
- Simplified parameter configurations
- Limited but essential tool access
- Reduced context window requirements

This tier sacrifices some advanced capabilities for increased reliability, ensuring users still receive helpful responses during partial outages.

### Tier 3: Minimal Model Strategy

If both primary and secondary models fail, the system can fall back to a minimal model focused on maximum reliability:

- Smaller, faster models (e.g., GPT-3.5-Turbo, Claude 3 Haiku, Gemma 2B)
- Bare minimum parameters
- No external tool dependencies
- Highly constrained context windows
- Potentially running locally rather than via API

This tier prioritizes availability over capability, ensuring basic functionality remains even during significant outages.

### Tier 4: Rule-Based Fallback

The final safety net is a completely deterministic, rule-based system that requires no LLM access:

- Pre-written responses for common scenarios
- Pattern matching for query classification
- Static content delivery
- Clear communication about limited functionality
- Potentially offering alternative contact methods

This tier ensures users receive some value and understand the situation even when all LLM capabilities are unavailable.

## Implementing Primary Model Strategy

The primary model strategy focuses on maximizing capabilities while implementing appropriate error handling and monitoring.

### Configuration and Setup

```python
def configure_primary_model(config):
    """Configure the primary LLM model with optimal settings"""
    primary_config = {
        "model": config.primary_model_name,  # e.g., "gpt-4", "claude-3-opus-20240229"
        "temperature": 0.7,  # Balanced creativity and determinism
        "max_tokens": 1024,  # Generous token limit for comprehensive responses
        "top_p": 0.95,  # Slight filtering of low-probability tokens
        "frequency_penalty": 0.0,  # No specific repetition penalty
        "presence_penalty": 0.0,  # No specific topic steering
        "timeout": 30,  # Longer timeout for complex processing
        "retry_count": 2,  # Limited retries to avoid delaying fallback
        "streaming": True  # Enable streaming for better user experience
    }
    
    # Add any model-specific parameters
    if "gpt" in config.primary_model_name:
        primary_config["n"] = 1
    elif "claude" in config.primary_model_name:
        primary_config["anthropic_version"] = "bedrock-2023-05-31"
    
    return primary_config
```

### Error Handling

Effective error handling for the primary model should:

1. Distinguish between different error types
2. Apply appropriate retry strategies
3. Log detailed information for debugging
4. Trigger fallbacks when necessary

```python
async def call_primary_model(prompt, config, context=None):
    """Call the primary model with comprehensive error handling"""
    primary_config = configure_primary_model(config)
    client = get_llm_client(primary_config["model"])
    
    try:
        # Attempt to call the primary model
        start_time = time.time()
        response = await client.generate(
            prompt=prompt,
            **{k: v for k, v in primary_config.items() if k != "model"}
        )
        latency = time.time() - start_time
        
        # Log successful response
        logger.info(
            f"Primary model response successful",
            extra={
                "model": primary_config["model"],
                "latency": latency,
                "tokens": response.usage.total_tokens if hasattr(response.usage, "total_tokens") else None,
                "context_id": context.get("request_id") if context else None
            }
        )
        
        return {
            "text": response.text,
            "model_used": primary_config["model"],
            "latency_ms": latency * 1000,
            "fallback_used": False,
            "fallback_level": 0
        }
        
    except RateLimitError as e:
        # Handle rate limiting - typically not retried as it will likely fail again
        logger.warning(
            f"Primary model rate limited: {str(e)}",
            extra={"model": primary_config["model"], "error": "rate_limit"}
        )
        raise FallbackTriggerError("Rate limit exceeded") from e
        
    except TimeoutError as e:
        # Handle timeout - could be temporary or indicate model overload
        logger.warning(
            f"Primary model timeout: {str(e)}",
            extra={"model": primary_config["model"], "error": "timeout"}
        )
        raise FallbackTriggerError("Request timed out") from e
        
    except (ServiceUnavailableError, ConnectionError) as e:
        # Handle service issues - likely affecting all requests
        logger.error(
            f"Primary model service error: {str(e)}",
            extra={"model": primary_config["model"], "error": "service_unavailable"}
        )
        raise FallbackTriggerError("Service unavailable") from e
        
    except Exception as e:
        # Handle unexpected errors
        logger.error(
            f"Primary model unexpected error: {str(e)}",
            extra={"model": primary_config["model"], "error": "unexpected", "error_details": str(e)}
        )
        raise FallbackTriggerError(f"Unexpected error: {str(e)}") from e
```

### Performance Monitoring

Monitoring the primary model's performance helps identify issues before they cause complete failures:

```python
def monitor_primary_model_health(metrics_store, config, window_minutes=15):
    """Monitor primary model health to detect degradation"""
    # Get recent metrics
    recent_metrics = metrics_store.get_recent_metrics(
        model=config.primary_model_name,
        minutes=window_minutes
    )
    
    if not recent_metrics:
        return {"status": "unknown", "reason": "No recent data"}
    
    # Calculate key health indicators
    success_rate = sum(1 for m in recent_metrics if m["success"]) / len(recent_metrics)
    avg_latency = sum(m["latency"] for m in recent_metrics) / len(recent_metrics)
    error_counts = Counter(m["error_type"] for m in recent_metrics if not m["success"])
    
    # Evaluate health status
    status = "healthy"
    reason = None
    
    if success_rate < config.health_thresholds.min_success_rate:
        status = "degraded"
        reason = f"Success rate ({success_rate:.2%}) below threshold ({config.health_thresholds.min_success_rate:.2%})"
    
    if avg_latency > config.health_thresholds.max_avg_latency:
        status = "degraded"
        reason = f"Average latency ({avg_latency:.2f}s) above threshold ({config.health_thresholds.max_avg_latency:.2f}s)"
    
    # Check for concerning error patterns
    for error_type, count in error_counts.items():
        error_rate = count / len(recent_metrics)
        if error_rate > config.health_thresholds.max_error_rate:
            status = "degraded"
            reason = f"High rate of {error_type} errors ({error_rate:.2%})"
    
    return {
        "status": status,
        "reason": reason,
        "metrics": {
            "success_rate": success_rate,
            "avg_latency": avg_latency,
            "request_count": len(recent_metrics),
            "error_counts": dict(error_counts)
        }
    }
```

## Implementing Secondary Model Strategy

The secondary model strategy focuses on balancing capability and reliability, with simplified parameters and more aggressive error handling.

### Configuration and Parameter Simplification

```python
def configure_secondary_model(config):
    """Configure the secondary LLM model with simplified settings"""
    secondary_config = {
        "model": config.secondary_model_name,  # e.g., "gpt-3.5-turbo", "claude-3-sonnet"
        "temperature": 0.5,  # More deterministic than primary
        "max_tokens": 512,  # Reduced token limit
        "top_p": 0.85,  # More aggressive filtering
        "timeout": 15,  # Shorter timeout for faster fallback
        "retry_count": 3,  # More retries since this is our backup
        "streaming": True  # Maintain streaming for user experience
    }
    
    # Add any model-specific parameters
    if "gpt" in config.secondary_model_name:
        secondary_config["n"] = 1
    elif "claude" in config.secondary_model_name:
        secondary_config["anthropic_version"] = "bedrock-2023-05-31"
    
    return secondary_config
```

### Prompt Simplification

When falling back to the secondary model, simplifying the prompt can improve reliability:

```python
def simplify_prompt_for_secondary(original_prompt, context=None):
    """Simplify a prompt for the secondary model"""
    # If the prompt is structured (e.g., a list of messages), extract the core query
    if isinstance(original_prompt, list):
        # Extract the last user message as the core query
        for message in reversed(original_prompt):
            if message.get("role") == "user":
                core_query = message.get("content", "")
                break
        else:
            core_query = str(original_prompt)
    else:
        core_query = original_prompt
    
    # Create a simplified prompt that focuses on the essential task
    simplified_prompt = f"""Please provide a concise and helpful response to this query:

{core_query}

Keep your response clear and direct, focusing on the most important information."""
    
    return simplified_prompt
```

### Error Handling and Logging

Secondary model error handling should be more aggressive with retries and provide clear context about the fallback:

```python
async def call_secondary_model(original_prompt, config, context=None):
    """Call the secondary model with appropriate error handling"""
    secondary_config = configure_secondary_model(config)
    client = get_llm_client(secondary_config["model"])
    
    # Simplify the prompt for better reliability
    simplified_prompt = simplify_prompt_for_secondary(original_prompt, context)
    
    try:
        # Implement retry logic directly
        max_retries = secondary_config.pop("retry_count", 3)
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                start_time = time.time()
                response = await client.generate(
                    prompt=simplified_prompt,
                    **{k: v for k, v in secondary_config.items() if k != "model"}
                )
                latency = time.time() - start_time
                
                # Log successful response
                logger.info(
                    f"Secondary model response successful",
                    extra={
                        "model": secondary_config["model"],
                        "latency": latency,
                        "retry_count": retry_count,
                        "context_id": context.get("request_id") if context else None
                    }
                )
                
                return {
                    "text": response.text,
                    "model_used": secondary_config["model"],
                    "latency_ms": latency * 1000,
                    "fallback_used": True,
                    "fallback_level": 1,
                    "original_error": context.get("original_error") if context else None
                }
                
            except (TimeoutError, ServiceUnavailableError, ConnectionError) as e:
                # These errors are retryable
                retry_count += 1
                if retry_count <= max_retries:
                    # Exponential backoff with jitter
                    wait_time = (2 ** retry_count) * 0.1 + (random.random() * 0.1)
                    logger.warning(
                        f"Secondary model error, retrying ({retry_count}/{max_retries}) after {wait_time:.2f}s: {str(e)}",
                        extra={"model": secondary_config["model"], "error": str(e)}
                    )
                    await asyncio.sleep(wait_time)
                else:
                    # Max retries exceeded
                    logger.error(
                        f"Secondary model failed after {max_retries} retries: {str(e)}",
                        extra={"model": secondary_config["model"], "error": str(e)}
                    )
                    raise FallbackTriggerError(f"Secondary model failed after retries: {str(e)}") from e
            
            except Exception as e:
                # Non-retryable errors
                logger.error(
                    f"Secondary model non-retryable error: {str(e)}",
                    extra={"model": secondary_config["model"], "error": str(e)}
                )
                raise FallbackTriggerError(f"Secondary model error: {str(e)}") from e
    
    except Exception as e:
        # Handle any errors not caught by the retry logic
        logger.error(
            f"Secondary model unexpected error: {str(e)}",
            extra={"model": secondary_config["model"], "error": "unexpected"}
        )
        raise FallbackTriggerError("All secondary model attempts failed") from e
```

## Implementing Minimal Model Strategy

The minimal model strategy prioritizes reliability over capability, using smaller models with highly constrained parameters.

### Configuration for Maximum Reliability

```python
def configure_minimal_model(config):
    """Configure the minimal LLM model for maximum reliability"""
    minimal_config = {
        "model": config.minimal_model_name,  # e.g., "gpt-3.5-turbo", "gemma-2b"
        "temperature": 0.3,  # Very deterministic
        "max_tokens": 256,  # Minimal token usage
        "top_p": 0.7,  # Aggressive filtering
        "timeout": 10,  # Very short timeout
        "retry_count": 5,  # Maximum retries
        "streaming": False  # Disable streaming for simplicity
    }
    
    # For local models, add specific configuration
    if config.minimal_model_is_local:
        minimal_config["local_model_path"] = config.local_model_path
    
    return minimal_config
```

### Extreme Prompt Simplification

For the minimal model, prompts should be as simple and direct as possible:

```python
def create_minimal_prompt(original_prompt, context=None):
    """Create an extremely simplified prompt for the minimal model"""
    # Extract the core question or instruction
    if isinstance(original_prompt, list):
        # For chat format, extract just the last user query
        for message in reversed(original_prompt):
            if message.get("role") == "user":
                core_query = message.get("content", "")
                # Extract just the first paragraph or sentence
                core_query = core_query.split('\n')[0].split('. ')[0]
                break
        else:
            core_query = "Please provide a helpful response."
    else:
        # For text format, take just the first paragraph
        core_query = original_prompt.split('\n')[0]
    
    # Create a minimal prompt with clear instructions
    minimal_prompt = f"""Question: {core_query}

Provide a brief, direct answer using simple language. Focus only on the most essential information."""
    
    return minimal_prompt
```

### Aggressive Error Handling

The minimal model implementation should include aggressive error handling with multiple fallback attempts:

```python
async def call_minimal_model(original_prompt, config, context=None):
    """Call the minimal model with maximum reliability measures"""
    minimal_config = configure_minimal_model(config)
    
    # Determine if we're using a local or API model
    if config.minimal_model_is_local:
        client = get_local_llm_client(minimal_config["local_model_path"])
    else:
        client = get_llm_client(minimal_config["model"])
    
    # Create a minimal prompt
    minimal_prompt = create_minimal_prompt(original_prompt, context)
    
    # Track attempts across different model options
    model_options = [
        minimal_config["model"],  # Primary minimal option
        config.minimal_model_fallback,  # Secondary minimal option
        "local-fallback"  # Last resort if available
    ]
    
    # Try each model option in sequence
    for model_option in model_options:
        if model_option is None:
            continue
            
        try:
            # Configure for this specific model option
            current_config = minimal_config.copy()
            current_config["model"] = model_option
            
            # Implement retry logic
            max_retries = current_config.pop("retry_count", 5)
            retry_count = 0
            
            while retry_count <= max_retries:
                try:
                    start_time = time.time()
                    
                    # Special handling for local fallback
                    if model_option == "local-fallback" and hasattr(config, "local_fallback_path"):
                        client = get_local_llm_client(config.local_fallback_path)
                    
                    response = await client.generate(
                        prompt=minimal_prompt,
                        **{k: v for k, v in current_config.items() 
                           if k not in ["model", "local_model_path"]}
                    )
                    latency = time.time() - start_time
                    
                    # Log successful response
                    logger.info(
                        f"Minimal model response successful with {model_option}",
                        extra={
                            "model": model_option,
                            "latency": latency,
                            "retry_count": retry_count,
                            "fallback_level": 2,
                            "context_id": context.get("request_id") if context else None
                        }
                    )
                    
                    return {
                        "text": response.text,
                        "model_used": model_option,
                        "latency_ms": latency * 1000,
                        "fallback_used": True,
                        "fallback_level": 2,
                        "original_error": context.get("original_error") if context else None
                    }
                    
                except Exception as e:
                    # Any error triggers a retry
                    retry_count += 1
                    if retry_count <= max_retries:
                        # Exponential backoff with jitter
                        wait_time = min((2 ** retry_count) * 0.1 + (random.random() * 0.1), 2.0)
                        logger.warning(
                            f"Minimal model {model_option} error, retrying ({retry_count}/{max_retries}): {str(e)}",
                            extra={"model": model_option, "error": str(e)}
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        # Max retries exceeded, try next model option
                        logger.error(
                            f"Minimal model {model_option} failed after {max_retries} retries",
                            extra={"model": model_option, "error": str(e)}
                        )
                        break  # Try next model option
        
        except Exception as e:
            # Log failure for this model option
            logger.error(
                f"Minimal model {model_option} unexpected error: {str(e)}",
                extra={"model": model_option, "error": "unexpected"}
            )
            # Continue to next model option
    
    # If we get here, all minimal model options failed
    logger.critical(
        "All minimal model options failed, falling back to rule-based response",
        extra={"context_id": context.get("request_id") if context else None}
    )
    raise FallbackTriggerError("All minimal model attempts failed")
```

## Implementing Rule-Based Fallback

The rule-based fallback provides a final safety net when all LLM options fail, using deterministic logic to generate responses.

### Pattern Matching for Common Queries

```python
def classify_query_intent(query):
    """Classify the intent of a user query using pattern matching"""
    query = query.lower()
    
    # Define patterns for common query types
    patterns = {
        "greeting": [
            r"hello", r"hi there", r"hey", r"greetings", r"good (morning|afternoon|evening)"
        ],
        "help": [
            r"help", r"how (do|can) I", r"what (can|do) you do", r"assist me"
        ],
        "information": [
            r"what is", r"tell me about", r"explain", r"describe", r"information on"
        ],
        "troubleshooting": [
            r"(not|isn't) working", r"problem with", r"error", r"issue", r"trouble", r"fix"
        ],
        "contact": [
            r"speak to (a|an|the) (human|person|agent|representative)", 
            r"contact (support|service|help)", r"talk to someone"
        ]
    }
    
    # Check each pattern category
    for intent, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, query):
                return intent
    
    # Default intent if no patterns match
    return "general"
```

### Static Response Templates

```python
def get_rule_based_response(query, context=None):
    """Generate a rule-based response based on query classification"""
    # Classify the query intent
    intent = classify_query_intent(query)
    
    # Define response templates for each intent
    templates = {
        "greeting": [
            "Hello! I'm currently operating in fallback mode due to technical limitations. I can provide basic assistance, but some features may be unavailable.",
            "Hi there! I'm running in a limited capacity right now. I'll do my best to help with basic questions."
        ],
        "help": [
            "I can provide basic information and assistance, though I'm currently operating in fallback mode with limited capabilities. For complex issues, you might want to try again later or contact support directly.",
            "While operating in fallback mode, I can help with simple questions and provide general guidance. For more complex assistance, please try again later when full service is restored."
        ],
        "information": [
            "I'm currently operating in fallback mode and can't provide detailed information on that topic. Basic information might be available on our help center at [help URL], or please try again later when full service is restored.",
            "Due to technical limitations, I can only provide basic information right now. For detailed information on this topic, please check our knowledge base or try again later."
        ],
        "troubleshooting": [
            "I'm sorry to hear you're experiencing an issue. While I'm operating in fallback mode with limited capabilities, here are some general troubleshooting steps: 1) Refresh the page, 2) Clear your browser cache, 3) Try again in a few minutes. If the problem persists, please contact support at [support email/phone].",
            "While I'm in fallback mode, I can suggest basic troubleshooting: restart the application, check your internet connection, and ensure you're using the latest version. For more specific help, please try again later or contact our support team."
        ],
        "contact": [
            "You can reach our support team at [support email/phone]. They're available [hours] to assist you directly. Please mention reference code [REF-FALLBACK] when contacting them.",
            "Our customer service team is available at [contact details] during [business hours]. They'll be happy to help you with your inquiry."
        ],
        "general": [
            "I'm currently operating in fallback mode with limited capabilities due to technical issues. I can help with basic questions, but for more complex assistance, please try again later or contact our support team at [support contact].",
            "Thanks for your message. I'm running in fallback mode right now, which limits my abilities. For urgent matters, please contact [support contact] or try again later when full service is restored."
        ]
    }
    
    # Select a template for the identified intent
    available_templates = templates.get(intent, templates["general"])
    selected_template = random.choice(available_templates)
    
    # Customize the template if context is available
    if context and hasattr(context, "support_contact"):
        selected_template = selected_template.replace("[support contact]", context.support_contact)
        selected_template = selected_template.replace("[support email/phone]", context.support_contact)
    
    if context and hasattr(context, "help_url"):
        selected_template = selected_template.replace("[help URL]", context.help_url)
    
    # Generate a reference code for support follow-up
    ref_code = f"REF-{uuid.uuid4().hex[:8].upper()}"
    selected_template = selected_template.replace("[REF-FALLBACK]", ref_code)
    
    # Log the fallback response
    logger.info(
        f"Generated rule-based fallback response for intent: {intent}",
        extra={
            "intent": intent,
            "ref_code": ref_code,
            "context_id": context.get("request_id") if context else None
        }
    )
    
    return {
        "text": selected_template,
        "model_used": "rule_based_fallback",
        "latency_ms": 0,  # Negligible latency for rule-based responses
        "fallback_used": True,
        "fallback_level": 3,
        "ref_code": ref_code,
        "intent": intent
    }
```

### Fallback Notification System

When using rule-based fallbacks, it's important to notify the appropriate teams:

```python
def notify_fallback_usage(fallback_data, config):
    """Notify appropriate teams about fallback usage"""
    # Determine severity based on fallback level and frequency
    if fallback_data["fallback_level"] == 3:  # Rule-based fallback
        severity = "high"
    elif fallback_data["fallback_level"] == 2:  # Minimal model
        severity = "medium"
    else:  # Secondary model
        severity = "low"
    
    # Create notification message
    message = f"Fallback activated: Level {fallback_data['fallback_level']} ({fallback_data['model_used']})\n"
    message += f"Reference Code: {fallback_data.get('ref_code', 'N/A')}\n"
    message += f"Intent: {fallback_data.get('intent', 'Unknown')}\n"
    message += f"Original Error: {fallback_data.get('original_error', 'Unknown')}\n"
    message += f"Timestamp: {datetime.now().isoformat()}"
    
    # Send notification based on configured channels
    if severity == "high" and config.notifications.slack_webhook:
        send_slack_notification(
            webhook=config.notifications.slack_webhook,
            channel=config.notifications.slack_channel,
            message=message,
            severity=severity
        )
    
    if severity in ["high", "medium"] and config.notifications.email:
        send_email_notification(
            recipients=config.notifications.email_recipients,
            subject=f"[{severity.upper()}] LLM Fallback Activated",
            body=message
        )
    
    # Log the notification
    logger.info(
        f"Fallback notification sent with severity: {severity}",
        extra={
            "fallback_level": fallback_data["fallback_level"],
            "model_used": fallback_data["model_used"],
            "severity": severity,
            "notification_channels": get_notification_channels(severity, config)
        }
    )
```

## Integrating the Complete Fallback System

Now that we've implemented each tier, let's integrate them into a complete fallback system.

### Main Fallback Orchestrator

```python
class FallbackManager:
    def __init__(self, config):
        self.config = config
        self.metrics_store = MetricsStore()
        self.logger = logging.getLogger("fallback_manager")
    
    async def process_with_fallbacks(self, prompt, context=None):
        """Process a request with the complete fallback hierarchy"""
        context = context or {}
        request_id = context.get("request_id", str(uuid.uuid4()))
        
        # Start with primary model
        try:
            # Check if primary model health indicates we should skip it
            health_status = monitor_primary_model_health(self.metrics_store, self.config)
            if health_status["status"] == "degraded" and self.config.auto_skip_degraded:
                self.logger.warning(
                    f"Skipping degraded primary model: {health_status['reason']}",
                    extra={"request_id": request_id}
                )
                raise FallbackTriggerError(f"Primary model degraded: {health_status['reason']}")
            
            # Try primary model
            response = await call_primary_model(prompt, self.config, context)
            
            # Record metrics for this successful primary call
            self.metrics_store.record_request(
                model=self.config.primary_model_name,
                success=True,
                latency=response["latency_ms"] / 1000,
                request_id=request_id
            )
            
            return response
            
        except FallbackTriggerError as e:
            # Record metrics for this failed primary call
            self.metrics_store.record_request(
                model=self.config.primary_model_name,
                success=False,
                error_type=str(e),
                request_id=request_id
            )
            
            # Update context with original error
            context["original_error"] = str(e)
            
            # Try secondary model
            try:
                response = await call_secondary_model(prompt, self.config, context)
                
                # Record metrics for this successful secondary call
                self.metrics_store.record_request(
                    model=self.config.secondary_model_name,
                    success=True,
                    latency=response["latency_ms"] / 1000,
                    request_id=request_id,
                    is_fallback=True,
                    fallback_level=1
                )
                
                return response
                
            except FallbackTriggerError as e:
                # Record metrics for this failed secondary call
                self.metrics_store.record_request(
                    model=self.config.secondary_model_name,
                    success=False,
                    error_type=str(e),
                    request_id=request_id,
                    is_fallback=True,
                    fallback_level=1
                )
                
                # Update context with latest error
                context["original_error"] = f"{context.get('original_error', '')} → {str(e)}"
                
                # Try minimal model
                try:
                    response = await call_minimal_model(prompt, self.config, context)
                    
                    # Record metrics for this successful minimal call
                    self.metrics_store.record_request(
                        model=response["model_used"],  # This might be one of
