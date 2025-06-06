"""
Main middleware class that combines all resilience features
"""

import time
import uuid
import logging
from typing import Dict, Any

from models.request import LLMRequest
from models.response import LLMResponse
from utils.logging import setup_logger
from utils.text_utils import sanitize_text
from resilience.circuit_breaker import create_circuit_breaker
from resilience.fallbacks import rule_based_fallback, call_llm_with_fallbacks
from monitoring.performance import monitor_performance
from monitoring.stats import StatsTracker
from circuitbreaker import CircuitBreakerError


class LLMMiddleware:
    """
    Main middleware class that combines all resilience features
    """

    def __init__(self):
        self.logger = setup_logger()
        # Initialize stats tracker for request analysis
        self.stats_tracker = StatsTracker()

    @create_circuit_breaker(failure_threshold=3, recovery_timeout=30)
    def protected_llm_call(self, request: LLMRequest) -> LLMResponse:
        """Protected LLM call with circuit breaker"""
        return call_llm_with_fallbacks(request)

    def process_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Process an LLM request with all resilience features

        Parameters:
        - prompt: The text prompt to send to the LLM
        - **kwargs: Additional parameters like temperature, max_tokens, etc.
          Special test parameters:
          - _test_force_first_fallback_fail: Force the first fallback to fail
          - _test_force_all_models_fail: Force all models to fail
          - _simulate_high_load: Simulate high load conditions

        Returns:
        - The LLM response with metadata
        """
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

        except Exception as e:
            self.logger.error(
                f"Error processing request: {str(e)}", extra={"request_id": request_id}
            )
            fallback_result = rule_based_fallback(prompt, request_id)
            return fallback_result

    def get_recent_performance(self) -> Dict[str, Any]:
        """Get performance statistics from recent requests"""
        return self.stats_tracker.get_recent_performance()

    def get_model_usage_stats(self) -> Dict[str, Any]:
        """Get statistics about which models are being used"""
        return self.stats_tracker.get_model_usage_stats()
