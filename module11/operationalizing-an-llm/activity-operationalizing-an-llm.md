# Activity: Building a Resilient LLM Application with Comprehensive Monitoring

## Overview

In this hands-on coding activity, you'll build a production-ready middleware for integrating Large Language Models (LLMs) into applications. You'll implement industry-standard resilience patterns including circuit breakers to prevent cascading failures, tiered fallback mechanisms for graceful degradation, comprehensive logging for debugging, and performance monitoring for anomaly detection. Through practical implementation of these patterns, you'll learn how to create stable, reliable AI integrations that can withstand the challenges of real-world production environments.



## Learning Objectives

By the end of this activity, you will be able to:
1. Implement circuit breaker patterns to prevent system overload when external services fail
2. Design tiered fallback mechanisms that degrade functionality gracefully
3. Create comprehensive logging that captures the full interaction lifecycle
4. Develop middleware patterns that properly isolate credentials and handle errors
5. Implement monitoring to detect anomalies in LLM performance and behavior



## Time Estimate

120 minutes



## Prerequisites

- Python 3.10 or higher
- Basic understanding of Python and API integrations
- Familiarity with LLMs and their APIs
- A code editor (VS Code recommended)
- Ollama with the following Gemma models installed
	- Gemma 3 4B (gemma3:4b)
	- Gemma 3 1B (gemma1:1b)
	- Gemma 2 2B (gemma:2b)


## Setup Instructions

### Step 1: Create a Project Directory

Create a new folder for your project:

```bash
mkdir llm-resilient-app
cd llm-resilient-app
```



### Step 2: Create and Activate a Virtual Environment

Create and activate a virtual environment for your project:

- **Mac/Linux**:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **Windows (PowerShell)**:

  ```bash
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt)**:

  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```



### Step 3: Install Dependencies

With the virtual environment active, install the required packages from the requirements.txt file:

```bash
pip install -r requirements.txt
```

The requirements.txt file contains the following dependencies:

```
colorlog==6.7.0
python-dotenv==1.0.0
tenacity==8.2.3
circuitbreaker==1.4.0
pydantic==1.10.8
requests==2.32.3
```



### Step 4: Configure Environment

1. Create a `.env` file in your project root:

   ```
   OPENAI_API_KEY=your_api_key_here
   # Or if using Ollama
   OLLAMA_API_URL=http://localhost:11434
   ```

2. Create a `.env.template` file as a reference:

   ```
   OPENAI_API_KEY=your_api_key_here
   # Or if using Ollama
   OLLAMA_API_URL=http://localhost:11434
   ```

3. Set up the basic project structure with the starter code provided by your instructor.



## Key Concepts

### Resilience Patterns

Production LLM applications need to handle various failure scenarios gracefully:

1. **Circuit Breakers**: Prevent cascading failures by automatically stopping requests to failing services after a threshold of failures is reached, allowing the system to recover.

2. **Tiered Fallbacks**: Provide alternative response mechanisms when primary systems fail:
   - Primary model with full parameters
   - Backup model with simplified parameters
   - Rule-based fallback that doesn't require LLM

3. **Retry Mechanisms**: Attempt operations multiple times with exponential backoff before giving up, handling transient errors effectively.

For a detailed guide on implementing tiered fallbacks, see [Tiered Fallback Mechanisms Guide](resources/tiered_fallback_mechanisms_guide.md).

### Comprehensive Logging

Effective monitoring of LLM interactions requires detailed logs:

1. **Structured Logging**: Organize log data with consistent fields to facilitate analysis and filtering.

2. **Request Correlation**: Track individual requests through their entire lifecycle using unique identifiers.

3. **Context Preservation**: Include relevant context with each log entry to understand the complete picture.

4. **Privacy Protection**: Sanitize sensitive information before logging to maintain security and compliance.

### Performance Monitoring

Understanding LLM performance requires tracking key metrics:

1. **Latency Tracking**: Measure response times for requests to identify performance issues.

2. **Token Usage**: Monitor token consumption for cost control and optimization.

3. **Anomaly Detection**: Identify unusual patterns in LLM behavior using statistical methods.

4. **Fallback Rates**: Track how often fallback mechanisms are triggered to assess system health.

For advanced anomaly detection techniques, refer to [LLM Anomaly Detection Techniques](resources/llm_anomaly_detection_techniques.md).



## Activity Tasks

### Task 1: Understanding the Starter Code (15 minutes)

Your first task is to familiarize yourself with the provided starter code to understand the architecture of the LLM middleware system. Read the see [LLM Middleware Architecture Overview](resources/llm_middleware_architecture_overview.md) guide get a grasp of how all the components work together in a production-ready LLM middleware system, then turn direct your attention to the provided code.

Begin by exploring the project structure:

1. **Core Orchestrator**: Examine the `middleware.py` file, which serves as the central component that coordinates all resilience features and connects various components.
    
2. **Data Models**: Review the `models` directory to understand the Pydantic models used for requests (`LLMRequest`) and responses (`LLMResponse`), which provide type safety and validation.
    
3. **Resilience Patterns**: Explore the `resilience` directory which contains:    
    - Circuit breaker implementation (`circuit_breaker.py`)
    - Fallback mechanisms (`fallbacks.py`) with rule-based and tiered model fallbacks
    - Retry logic architecture (placeholder in `retry.py`)

4. **Monitoring & Observability**: Examine the `monitoring` directory to understand:    
    - Performance metrics tracking (`performance.py`)
    - Anomaly detection framework (`anomaly.py`)
    - Request statistics collection (`stats.py`)

5. **API Integration**: Look at the `api` directory to understand how the system connects to actual LLM services.
    
6. **Utilities**: Review the `utils` directory for helper functions related to logging, text sanitization, and serialization.

After reviewing the code structure, run the starter application using `python main.py` to see the current implementation state. You'll notice it fails with an error about the unimplemented circuit breaker functionality, as this feature will be your next task to implement.

Pay particular attention to the TODOs in the code, especially in:

- `circuit_breaker.py`: Implementing the circuit breaker pattern
- `fallbacks.py`: Creating a tiered fallback system
- `performance.py`: Adding comprehensive metrics tracking
- `middleware.py`: Connecting all components for end-to-end functionality

This initial exploration will give you the necessary context to implement the resilience features in subsequent tasks, starting with the circuit breaker pattern.


Task 2: Implementing Circuit Breakers (20 minutes)

2. We'll begin writing code with this task by implementing the circuit breaker pattern. It is an important resilience feature that prevents cascading failures in distributed systems. 
   
   Open the `resilience/circuit_breaker.py` file and locate the `create_circuit_breaker` function. This function will serve as a decorator factory that wraps API calls with circuit breaker protection. 

    **Step 2.1**. Find the TODO comment: "Implement the circuit breaker pattern:" and add this code snippet:
    
    ```python
    def decorator(func: Callable) -> Callable:
        # Apply the circuit breaker from the library
        @circuit(failure_threshold=failure_threshold, recovery_timeout=recovery_timeout)
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
    ```
    
    This code creates a decorator function that applies the circuit breaker pattern. It uses the `@circuit` decorator from the circuitbreaker library, configuring it with the failure threshold (number of failures before opening the circuit) and recovery timeout (seconds to wait before trying again) parameters. This function will serve as a decorator factory that wraps API calls with circuit breaker protection. 
    
    **Step 2.2**. Find the TODO comment: "Handle circuit states and errors properly:" and add this code snippet:
    
    ```python
            logger = logging.getLogger("llm_app")
            caller_info = inspect.getframeinfo(inspect.currentframe().f_back)
            request_id = kwargs.get("request_id", "unknown")

            logger.debug(
                f"Circuit breaker protecting call to {func.__name__} from {caller_info.function}",
                extra={"request_id": request_id},
            )

            try:
                return func(*args, **kwargs)
            except CircuitBreakerError as e:
                logger.warning(
                    f"Circuit open for {func.__name__}. Using fallback.",
                    extra={"request_id": request_id},
                )
                raise
            except Exception as e:
                logger.error(
                    f"Error in circuit-protected function {func.__name__}: {str(e)}",
                    extra={"request_id": request_id},
                )
                raise
    ```
    
    This code implements error handling within the wrapper function. It distinguishes between CircuitBreakerError exceptions (which occur when the circuit is already open) and other exceptions. When catching a CircuitBreakerError, it logs a warning message explaining that the circuit is open. For other exceptions, it logs detailed error information but allows the exception to propagate up. When calls succeed, it simply returns the original function's result.
    
    **Step 2.3**. Find the TODO comment: "Add detailed logging:" and add this code snippet:
    
    ```python
        return wrapper

    return decorator
    ```
    
    This code completes the decorator factory function by returning the wrapper function and the decorator itself. The logging is already implemented in the previous step, where it includes the function name being protected, records state transitions, includes the request_id in all log messages, and uses appropriate log levels (warning for circuit open, error for other failures).
    
    This implementation will provide a robust protection mechanism that prevents system overload during failure scenarios.


### Task 3: Adding Tiered Fallback Mechanisms (20 minutes)

In this task, we'll implement a complete tiered fallback system with two components: a rule-based fallback and a multi-tier model fallback strategy.

1. First, implement the `rule_based_fallback` function which serves as the final safety net when all LLM models fail. This function should:
	
	- Accept a prompt and request ID as input
	- Log appropriate warning messages
	- Use keyword matching to provide context-aware responses when possible
	- Return a default fallback response with appropriate metadata when no keywords match

   **Step 3.1**. Find the TODO comment: "Implement the rule-based fallback system" and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "Set up logging with a warning message that indicates fallback is being used" and add this code snippet:
    
    ```python
    logger = logging.getLogger("llm_app")
    logger.warning(
        f"Using rule-based fallback for prompt", extra={"request_id": request_id}
    )
    ```
    
    This code creates a logger and logs a warning message indicating that the rule-based fallback is being used, including the request ID for traceability.
    
    **Step 3.3**. Find the TODO comment: "Print a console message indicating the fallback system is responding" and add this code snippet:
    
    ```python
    print("\n[Response from rule-based fallback system]")
    ```
    
    This code prints a message to the console to clearly indicate that the response is coming from the fallback system rather than an LLM.
    
    **Step 3.4**. Find the TODO comment: "Create a dictionary of keywords mapped to appropriate fallback responses" and add this code snippet:
    
    ```python
    # Simple keyword-based response selection
    keywords = {
        "hello": "Hello! I'm currently operating in fallback mode due to service limitations.",
        "help": "I'd like to help, but I'm currently in fallback mode with limited capabilities.",
        "explain": "I'm sorry, but I can't provide explanations right now as I'm in fallback mode.",
        "how to": "I apologize, but I can't provide how-to instructions at the moment.",
    }
    ```
    
    This code creates a dictionary that maps common keywords to appropriate fallback responses, allowing the system to provide somewhat context-aware responses even in fallback mode.
    
    **Step 3.5**. Find the TODO comment: "Check if any keywords match the user's prompt (case-insensitive)" and add this code snippet:
    
    ```python
    # Check for keyword matches
    prompt_lower = prompt.lower()
    for keyword, response in keywords.items():
        if keyword in prompt_lower:
            print(response)  # Print response to console
            return {
                "text": response,
                "model_used": "rule_based_fallback",
                "tokens_used": 0,
                "latency_ms": 0,
                "fallback_used": True,
                "fallback_level": 2,
                "request_id": request_id,
            }
    ```
    
    This code converts the user's prompt to lowercase, then checks if any of the keywords are present in the prompt. If a match is found, it prints and returns the corresponding response along with metadata.
    
    **Step 3.6**. Find the TODO comment: "If no keywords match, create a list of generic fallback responses" and add this code snippet:
    
    ```python
    # Default fallback responses if no keywords match
    fallback_responses = [
        "I'm sorry, I'm having trouble processing your request right now.",
        "Our AI service is currently experiencing issues. Please try again later.",
        "I apologize, but I'm unable to generate a response at this moment.",
    ]

    response = random.choice(fallback_responses)
    print(response)  # Print response to console
    ```
    
    This code creates a list of generic fallback responses and randomly selects one to use when no keywords match the user's prompt, then prints it to the console.
    
    **Step 3.7**. Find the TODO comment: "Return a complete response dictionary with:" and add this code snippet:
    
    ```python
    return {
        "text": response,
        "model_used": "rule_based_fallback",
        "tokens_used": 0,
        "latency_ms": 0,
        "fallback_used": True,
        "fallback_level": 2,
        "request_id": request_id,
    }
    ```
    
    This code returns a dictionary containing the fallback response text and metadata, including information about the fallback level and request ID for tracking purposes.


2. Next, implement the `call_llm_with_fallbacks` function which creates a graceful degradation path when the primary LLM model fails.

    **Step 3.8**. Find the TODO comment: "Implement the primary model call with try-except handling" and add this code snippet:
    
    ```python
    # Try primary model first
    try:
        # For testing: if we're forcing all models to fail, raise an exception immediately
        if force_all_models_fail:
            logger.info(
                f"Simulating failure in primary model due to test flag",
                extra={"request_id": request.request_id},
            )
            raise ValueError("Simulated failure in primary model for testing")

        logger.info(
            f"Attempting primary model: {request.model}",
            extra={"request_id": request.request_id},
        )
        result = call_llm_api(request)
        return LLMResponse(**result)
    ```
    
    This code attempts to call the primary model (which should be gemma3:4b as specified in the original request) with the full set of parameters. It includes test flag handling and logs the attempt. If successful, it returns the response directly.

    **Step 3.9**. Find the TODO comment: "Implement the first fallback level" and add this code snippet:
    
    ```python
    except Exception as primary_error:
        logger.warning(
            f"Primary model failed: {str(primary_error)}. Trying first fallback model.",
            extra={"request_id": request.request_id},
        )

        # Try first fallback model with simplified parameters
        try:
            # For testing: if we're forcing all models to fail, raise an exception
            if force_all_models_fail or force_first_fallback_fail:
                logger.info(
                    f"Simulating failure in first fallback model due to test flag",
                    extra={"request_id": request.request_id},
                )
                raise ValueError(
                    "Simulated failure in first fallback model for testing"
                )

            # Create a simplified request for the first fallback model
            fallback_request = LLMRequest(
                prompt=request.prompt,
                max_tokens=min(request.max_tokens, 50),  # Reduce token count
                temperature=0.3,  # Lower temperature for more predictable results
                model="gemma3:1b",  # Use a more reliable model as fallback
                request_id=request.request_id,
            )

            result = call_llm_api(fallback_request)
            result["fallback_used"] = True
            result["fallback_level"] = 1
            return LLMResponse(**result)
        ```
        
    This code implements the first fallback tier when the primary model fails. It logs the failure, creates a modified request with more conservative parameters (reduced max_tokens, lower temperature), and specifically changes the model to "gemma3:1b" which is a smaller, potentially more reliable model. It adds metadata to indicate a fallback was used.

    **Step 3.10**. Find the TODO comment: "Implement the second fallback level" and add this code snippet:
    
    ```python
        except Exception as first_fallback_error:
            logger.warning(
                f"First fallback model failed: {str(first_fallback_error)}. Trying second fallback model.",
                extra={"request_id": request.request_id},
            )

            # Try second fallback model with even more simplified parameters
            try:
                # For testing: if we're forcing all models to fail, raise an exception
                if force_all_models_fail:
                    logger.info(
                        f"Simulating failure in second fallback model due to test flag",
                        extra={"request_id": request.request_id},
                    )
                    raise ValueError(
                        "Simulated failure in second fallback model for testing"
                    )

                # Create an even more simplified request for the second fallback model
                second_fallback_request = LLMRequest(
                    prompt=request.prompt,
                    max_tokens=min(
                        request.max_tokens, 30
                    ),  # Further reduce token count
                    temperature=0.1,  # Even lower temperature for most predictable results
                    model="gemma:2b",  # Use the smallest model as final fallback
                    request_id=request.request_id,
                )

                result = call_llm_api(second_fallback_request)
                result["fallback_used"] = True
                result["fallback_level"] = 2
                return LLMResponse(**result)
            ```
            
    This code implements the second fallback tier with even more conservative parameters when the first fallback also fails. It creates another request with further reduced max_tokens, very low temperature, and specifically uses "gemma:2b" as the model—the smallest and most reliable option available.

    **Step 3.11**. Find the TODO comment: "Implement the final rule-based fallback" and add this code snippet:
    
    ```python
            except Exception as second_fallback_error:
                logger.error(
                    f"Second fallback model also failed: {str(second_fallback_error)}. Using rule-based fallback.",
                    extra={"request_id": request.request_id},
                )

                # Use rule-based fallback as last resort
                result = rule_based_fallback(request.prompt, request.request_id)
                return LLMResponse(**result)
    ```
    
    This code implements the final rule-based fallback as a safety net when all model-based approaches fail. It logs the comprehensive failure and calls the rule_based_fallback function as the last resort when all three LLM models (gemma3:4b, gemma3:1b, and gemma:2b) have failed.


### Task 4: Enhancing the Logging System (15 minutes)

In this next task, we'll implement a logging system that provides visibility into the entire request lifecycle and helps with debugging and monitoring. 

Open the `utils/logging.py` file and locate the `setup_logger` function. This function creates and configures the logging system used throughout the application.

**Step 4.1**. Find the TODO comment: "Enhance the setup_logger function:" and follow the steps below.

   **Step 4.2**. Find the TODO comment: "1. Modify the log formatters to include request_id in a consistent position" and add this code snippet:

   ```python
    # Create a custom logger
    logger = logging.getLogger("llm_app")

    # Clear any existing handlers
    if logger.handlers:
        logger.handlers = []

    # Set the logging level
    logger.setLevel(logging.DEBUG)
    ```

   This code creates a new logger named "llm_app", clears any existing handlers to avoid duplicate logs, and sets the logging level to DEBUG to capture all log messages.

   **Step 4.3**. Find the TODO comment: "2. Ensure the format includes: timestamp, log level, request_id, module, line number, and message" and add this code snippet:

   ```python
    # Create console handler with colored output
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] [%(request_id)s] %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )

    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    ```

   This code creates a console handler with colored output for better readability. The formatter includes timestamp, log level, request_id, module name, line number, and the message, all in a structured format. Different log levels are assigned different colors to make them visually distinct.

   **Step 4.4**. Find the TODO comment: "3. Add color coding for different log levels (DEBUG=cyan, INFO=green, WARNING=yellow, ERROR=red, CRITICAL=red with background)" and add this code snippet:

   ```python
    # Create file handler for persistent logging
    file_handler = logging.FileHandler("llm_app.log")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(request_id)s] %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    ```

   This code creates a file handler that writes logs to "llm_app.log" for persistent storage. The file logs include the same structured information as the console logs but without color coding. Both handlers are added to the logger.

   **Step 4.5**. Find the TODO comment: "Implement context tracking across components:" and add this code snippet:

   ```python
    # Create a filter to add request_id to log records
    context_filter = ContextFilter()
    logger.addFilter(context_filter)

    # Add the filter to the logger to provide a default request_id
    logger.context_filter = context_filter
    ```

   This code creates a ContextFilter instance and adds it to the logger. The filter will automatically add the current request_id to any log record that doesn't already have one. The filter is also attached directly to the logger object so other components can access it.

   **Step 4.6**. Find the TODO comment: "Test your enhanced logging by adding a debug message in setup_logger:" and add this code snippet:

   ```python
    return logger
    ```

   This code returns the configured logger object so it can be used throughout the application. The logger now includes structured logging with request_id tracking, color-coded console output, and persistent file logging.


### Task 5: Adding Performance Monitoring (15 minutes)

Now we're going to implement performance monitoring capabilities that track key metrics and detect anomalies in LLM behavior. Open the `monitoring/performance.py` file and locate the `monitor_performance` function. This function is called after each LLM request to analyze the response characteristics and identify potential issues. 

   **Step 5.1**. Find the TODO comment: "Implement comprehensive metrics tracking" and add this code snippet:

   ```python
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
    ```

   This code creates a PerformanceMetrics object to track key metrics. It estimates token usage by allocating approximately 50% to the prompt and 50% to the completion, records the latency from the response, and calculates the estimated cost using the calculate_token_cost function when not using a rule-based fallback.

   **Step 5.2**. Find the TODO comment: "Add anomaly detection integration" and add this code snippet:

   ```python
    # Update recent metrics for anomaly detection
    update_metrics_history(response.latency_ms, response.tokens_used)

    # Detect anomalies
    metrics.anomaly_score = detect_anomalies(metrics)
    ```

   This code integrates with the anomaly detection system by recording each new measurement using update_metrics_history, which builds a statistical baseline of normal behavior. It then calls detect_anomalies with the current metrics to get an anomaly score between 0 and 1 (higher values indicate more unusual behavior) and stores this score in the metrics object.

   **Step 5.3**. Find the TODO comment: "Implement conditional logging based on anomaly scores" and add this code snippet:

   ```python
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
    ```

   This code implements conditional logging based on the anomaly score. It uses INFO level logging for normal responses but switches to WARNING level for responses with anomaly scores above 0.7. The log message includes detailed performance data such as model name, token counts, latency, and estimated cost. For high anomaly scores, it adds an additional warning log entry with "ANOMALY DETECTED" to make these events stand out in the logs.

---

### Task 6: Creating a Complete Middleware Layer (20 minutes)

In our final task, we'll integrate all the components we've built into a cohesive middleware layer that orchestrates the entire LLM interaction process. Open the `middleware.py` file and examine the `LLMMiddleware` class, which serves as the central coordinator for all resilience features. 

   **Step 6.1**. Find the TODO comment: "Implement the protected_llm_call method with circuit breaker" and add this code snippet:

   ```python
    @create_circuit_breaker(failure_threshold=3, recovery_timeout=30)
    def protected_llm_call(self, request: LLMRequest) -> LLMResponse:
        """Protected LLM call with circuit breaker"""
        return call_llm_with_fallbacks(request)
    ```

   This code applies the circuit breaker decorator to protect LLM calls with a failure threshold of 3 and a recovery timeout of 30 seconds. The method calls the `call_llm_with_fallbacks` function with the request object, connecting your circuit breaker and fallback implementations.

   **Step 6.2**. Find the TODO comment: "Implement request processing setup" and add this code snippet:
   
   ```python
    # Generate a request ID for tracking
    request_id = str(uuid.uuid4())

    # Update the logger's context filter with the current request ID
    self.logger.context_filter.request_id = request_id

    self.logger.info(
        f"Processing request: '{prompt[:50]}...'", extra={"request_id": request_id}
    )

    # Extract test flags from kwargs
    test_force_first_fallback_fail = kwargs.pop(
        "_test_force_first_fallback_fail", False
    )
    test_force_all_models_fail = kwargs.pop("_test_force_all_models_fail", False)
    simulate_high_load = kwargs.pop("_simulate_high_load", False)

    # Create a validated request object
    request_data = kwargs.copy()
    request_data["prompt"] = prompt
    request_data["request_id"] = request_id

    # Add test flags to request data before creating the request object
    request_data["test_force_first_fallback_fail"] = test_force_first_fallback_fail
    request_data["test_force_all_models_fail"] = test_force_all_models_fail
    request_data["simulate_high_load"] = simulate_high_load
    ```

   This code sets up the request processing by generating a unique request ID, updating the logger's context, and extracting test flags from the kwargs. It then creates a request data dictionary with all necessary information.

   **Step 6.3**. Find the TODO comment: "Implement request validation and sanitization" and add this code snippet:

   ```python
    try:
        request = LLMRequest(**request_data)

        # Log if test flags are active
        if any(
            [
                test_force_first_fallback_fail,
                test_force_all_models_fail,
                simulate_high_load,
            ]
        ):
            self.logger.info(
                f"Test flags active: force_first_fail={test_force_first_fallback_fail}, "
                f"force_all_fail={test_force_all_models_fail}, "
                f"high_load={simulate_high_load}",
                extra={"request_id": request_id},
            )

        # Sanitize prompt before logging (remove sensitive data)
        sanitized_prompt = sanitize_text(prompt)
        self.logger.info(
            f"Validated request with sanitized prompt: '{sanitized_prompt[:50]}...'",
            extra={"request_id": request_id},
        )

        start_time = time.time()
    ```

   This code creates a validated request object, logs any active test flags, and sanitizes the prompt before logging to prevent sensitive information from appearing in logs.

   **Step 6.4**. Find the TODO comment: "Implement the try-except block to handle circuit breaker errors" and add this code snippet:

   ```python
    try:
        # Use the circuit breaker protected method
        response = self.protected_llm_call(request)
    except CircuitBreakerError:
        self.logger.warning(
            "Circuit breaker open, using rule-based fallback",
            extra={"request_id": request_id},
        )
        result = rule_based_fallback(prompt, request_id)
        response = LLMResponse(**result)
    ```

   This code adds specific handling for CircuitBreakerError exceptions, which occur when the circuit is already open due to previous failures. When catching this exception, it logs the condition with a warning message and immediately uses the rule-based fallback function instead of attempting further LLM calls.

   **Step 6.5**. Find the TODO comment: "Add performance monitoring and request tracking" and add this code snippet:

   ```python
    # Track request processing time
    processing_time = (time.time() - start_time) * 1000
    self.logger.info(
        f"Request processed in {processing_time:.2f}ms",
        extra={"request_id": request_id},
    )

    # Monitor performance
    metrics = monitor_performance(request, response)

    # Store recent request for analysis
    self.stats_tracker.store_request(request, response, metrics)

    return response.dict()
    ```

   This code connects all components for end-to-end functionality. It tracks and logs the request processing time, monitors performance by calling the `monitor_performance` function with the request and response objects, and stores the request data in the stats tracker for analysis.

   **Step 6.6**. Find the TODO comment: "Implement general exception handling" and add this code snippet:

   ```python
    except Exception as e:
        self.logger.error(
            f"Error processing request: {str(e)}", extra={"request_id": request_id}
        )
        fallback_result = rule_based_fallback(prompt, request_id)
        return fallback_result
    ```

   This code provides general exception handling for any errors that might occur during request processing, logging the error and using the rule-based fallback function to provide a response.

   **Step 6.7**. Find the TODO comment: "Implement the get_recent_performance method" and add this code snippet:

   ```python
    def get_recent_performance(self) -> Dict[str, Any]:
        """Get performance statistics from recent requests"""
        return self.stats_tracker.get_recent_performance()
    ```

   This method provides valuable insights into the system's behavior by retrieving and formatting statistics about recent requests, helping to identify trends or issues.

   **Step 6.8**. Find the TODO comment: "Implement the get_model_usage_stats method" and add this code snippet:

   ```python
    def get_model_usage_stats(self) -> Dict[str, Any]:
        """Get statistics about which models are being used"""
        return self.stats_tracker.get_model_usage_stats()
    ```

   This method retrieves statistics about which models are being used, providing insights into model usage patterns and helping to optimize resource allocation.



## Testing Your Implementation

After completing the activity tasks, you can test your implementation using:

```bash
python main.py
```

This will execute the demonstration code and show:
1. Normal LLM operations with full tracing
2. Fallback mechanisms when primary methods fail
3. Performance statistics across all test runs

You should see output similar to:

```
===== LLM Middleware Demo =====

----- Testing normal operation -----
[LLM response about circuit breakers]

Response metadata:
{
  "text": "Circuit breakers in software architecture prevent cascading failures by stopping operations when a service fails repeatedly. They allow graceful degradation and automatic recovery after a timeout period.",
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 42,
  "latency_ms": 1253.45,
  "fallback_used": false,
  "fallback_level": 0,
  "request_id": "8f7e6d5c-4b3a-2a1b-0c9d-8e7f6d5c4b3a",
  "timestamp": "2025-04-16T15:30:45.123456"
}

----- Testing fallback mechanism -----
[Fallback response about France]

Response metadata:
{
  "text": "Paris is the capital of France.",
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 8,
  "latency_ms": 876.54,
  "fallback_used": true,
  "fallback_level": 1,
  "request_id": "1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p",
  "timestamp": "2025-04-16T15:30:50.654321"
}

----- Performance statistics -----
{
  "request_count": 2,
  "avg_latency_ms": 1064.995,
  "max_latency_ms": 1253.45,
  "min_latency_ms": 876.54,
  "avg_tokens": 25.0,
  "total_tokens": 50,
  "fallback_rate": 0.5,
  "high_anomaly_count": 0
}

==== End of Demo ====
```



## Extension Options

If you complete the main activity and want to challenge yourself further:

1. **Enhanced Anomaly Detection**
   - Implement more sophisticated anomaly detection for LLM responses
   - Add content-based analysis to detect problematic outputs
   - Create an alert system that could notify operators about issues
   
   For detailed implementation guidance, see [LLM Anomaly Detection Techniques](resources/llm_anomaly_detection_techniques.md).

2. **Multi-Provider Fallback**
   - Extend the system to support multiple LLM providers (e.g., OpenAI, Anthropic, local models)
   - Create a strategy for selecting the best provider based on past performance
   - Implement failover between providers when one experiences issues
   
   For implementation strategies, refer to [Tiered Fallback Mechanisms Guide](resources/tiered_fallback_mechanisms_guide.md).

3. **Performance Dashboard**
   - Create a simple web dashboard to visualize the monitoring data
   - Add real-time performance graphs using a library like Dash or Streamlit
   - Implement historical performance tracking and trend analysis



## Conclusion

This activity focuses on implementing production-grade resilience features for LLM applications. By completing this activity, you'll gain practical experience with circuit breakers, tiered fallbacks, comprehensive logging, middleware patterns, and performance monitoring. These skills are essential for building reliable AI systems that can withstand the challenges of real-world usage and provide consistent service even when components fail.

### Further Reading

To deepen your understanding of the concepts covered in this activity, explore these additional resources:

- [LLM Middleware Architecture Overview](resources/llm_middleware_architecture_overview.md) - Comprehensive architectural overview of a production-ready LLM middleware system
- [Tiered Fallback Mechanisms Guide](resources/tiered_fallback_mechanisms_guide.md) - In-depth guide to implementing robust fallback strategies
- [LLM Anomaly Detection Techniques](resources/llm_anomaly_detection_techniques.md) - Advanced techniques for monitoring and detecting unusual LLM behavior
