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
    logger = logging.getLogger("llm_app")
    logger.warning(
        f"Using rule-based fallback for prompt", extra={"request_id": request_id}
    )

    print("\n[Response from rule-based fallback system]")

    # Simple keyword-based response selection
    keywords = {
        "hello": "Hello! I'm currently operating in fallback mode due to service limitations.",
        "help": "I'd like to help, but I'm currently in fallback mode with limited capabilities.",
        "explain": "I'm sorry, but I can't provide explanations right now as I'm in fallback mode.",
        "how to": "I apologize, but I can't provide how-to instructions at the moment.",
    }

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

    # Default fallback responses if no keywords match
    fallback_responses = [
        "I'm sorry, I'm having trouble processing your request right now.",
        "Our AI service is currently experiencing issues. Please try again later.",
        "I apologize, but I'm unable to generate a response at this moment.",
    ]

    response = random.choice(fallback_responses)
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

            except Exception as second_fallback_error:
                logger.error(
                    f"Second fallback model also failed: {str(second_fallback_error)}. Using rule-based fallback.",
                    extra={"request_id": request.request_id},
                )

                # Use rule-based fallback as last resort
                result = rule_based_fallback(request.prompt, request.request_id)
                return LLMResponse(**result)
