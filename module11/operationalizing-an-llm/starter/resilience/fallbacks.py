"""
Fallback mechanisms for when LLM calls fail
"""

import logging
import random
from typing import Dict, Any

from models.request import LLMRequest
from models.response import LLMResponse


def rule_based_fallback(prompt: str, request_id: str) -> Dict[str, Any]:
    """A rule-based fallback when LLM calls fail"""
    # TODO: Implement the rule-based fallback system

    # TODO: Set up logging with a warning message that indicates fallback is being used
    #    Include the request_id in the log's extra parameters for traceability

    # TODO: Print a console message indicating the fallback system is responding

    # TODO: Create a dictionary of keywords mapped to appropriate fallback responses
    # Include at least 4 different keywords (such as "hello", "help", "explain", "how to")
    # with appropriate responses that indicate limited functionality

    # TODO: Check if any keywords match the user's prompt (case-insensitive)
    # If a match is found, return that specific response with appropriate metadata

    # TODO: If no keywords match, create a list of generic fallback responses
    # and randomly select one to return

    # TODO: Return a complete response dictionary with:
    # - text: The fallback response text
    # - model_used: "rule_based_fallback"
    # - tokens_used: 0 (since no tokens are consumed)
    # - latency_ms: 0 (since no API call is made)
    # - fallback_used: True
    # - fallback_level: 2 (highest fallback level)
    # - request_id: The provided request_id

    return {}  # Replace with actual implementation


# This function will be imported from api.llm_client in the actual implementation
# We're declaring it here to avoid circular imports
def call_llm_api(request: LLMRequest) -> Dict[str, Any]:
    """Placeholder for the actual API call function"""
    pass


# The function declared above as a placeholder to prevent circular imports. The
# actual implementation is imported at runtime from api.llm_client. This pattern
# allows us to maintain proper type hints and function signatures while avoiding
# circular dependency issues when modules need to reference each other. The import
# occurs within function scope rather than at module level.


def call_llm_with_fallbacks(request: LLMRequest) -> LLMResponse:
    """
    Implement tiered fallback mechanisms

    Try multiple approaches in order:
    1. Primary model with full parameters (gemma3:4b)
    2. First fallback model with simplified parameters (gemma3:1b)
    3. Second fallback model with further simplified parameters (gemma:2b)
    4. Rule-based fallback

    Return the best possible response along with metadata
    """
    # This will be imported from api.llm_client in the actual implementation
    from api.llm_client import call_llm_api

    logger = logging.getLogger("llm_app")

    # Check for test flags
    force_first_fallback_fail = request.test_force_first_fallback_fail
    force_all_models_fail = request.test_force_all_models_fail
    simulate_high_load = request.simulate_high_load

    # If simulating high load, skip directly to the appropriate model based on query complexity
    if simulate_high_load:
        # Simple heuristic: use token count as a proxy for complexity
        if request.max_tokens <= 50:
            logger.info(
                f"System under high load, using smallest model (gemma:2b) for simple query",
                extra={"request_id": request.request_id},
            )
            request.model = "gemma:2b"
        elif request.max_tokens <= 100:
            logger.info(
                f"System under high load, using medium model (gemma3:1b) for moderate query",
                extra={"request_id": request.request_id},
            )
            request.model = "gemma3:1b"
        # For complex queries, still use the primary model

    # TODO: Implement the primary model call with try-except handling
    # 1. Call the LLM API with the original request parameters
    # 2. If successful, return the result as an LLMResponse
    # 3. If an exception occurs, catch it and proceed to the first fallback

    # TODO: Implement the first fallback level
    # 1. Log the primary model failure with details about the error
    # 2. Create a modified LLMRequest with:
    #    * The same prompt but reduced max_tokens (50 or less)
    #    * Lower temperature (0.3) for more predictable outputs
    #    * Model set to "gemma3:1b" as the first fallback option
    # 3. Call the API with this fallback request in another try-except block
    # 4. If successful, return the result with fallback metadata:
    #    * "fallback_used": True
    #    * "fallback_level": 1
    # 5. If this fails too, catch the exception and proceed to the second fallback

    # TODO: Implement the second fallback level
    # 1. Log the first fallback failure with error details
    # 2. Create an even more simplified LLMRequest with:
    #    * Further reduced max_tokens (30 or less)
    #    * Very low temperature (0.1) for maximum predictability
    #    * Model set to "gemma:2b" as the final model fallback option
    # 3. Call the API with this minimal request in another try-except block
    # 4. If successful, return the result with fallback metadata:
    #    * "fallback_used": True
    #    * "fallback_level": 2
    # 5. If this also fails, catch the exception and proceed to the rule-based fallback

    # TODO: Implement the final rule-based fallback
    # 1. Log that all model attempts have failed
    # 2. Call the rule_based_fallback function with the prompt and request_id
    # 3. Return the result as an LLMResponse
