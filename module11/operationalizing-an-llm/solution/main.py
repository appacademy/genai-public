"""
Example usage of the LLM middleware
"""

import json
from utils.serializers import datetime_json_serializer
from middleware import LLMMiddleware


def run_tests():
    """Run a series of tests to demonstrate the middleware functionality"""
    middleware = LLMMiddleware()

    print("\n" + "=" * 80)
    print("TEST 1: NORMAL OPERATION WITH PRIMARY MODEL (gemma3:4b)")
    print("=" * 80)
    response = middleware.process_request(
        "Explain the concept of circuit breakers in software architecture in 50 words or less.",
        max_tokens=150,
    )
    print(json.dumps(response, indent=2, default=datetime_json_serializer))

    print("\n" + "=" * 80)
    print("TEST 2: FALLBACK MECHANISM WITH NON-EXISTENT MODEL")
    print("=" * 80)
    response = middleware.process_request(
        "What is the capital of France?",
        model="non-existent-model",  # This will cause a fallback
        max_tokens=50,
    )
    print(json.dumps(response, indent=2, default=datetime_json_serializer))

    print("\n" + "=" * 80)
    print("TEST 3: USING GEMMA:2B AS PRIMARY MODEL")
    print("=" * 80)
    response = middleware.process_request(
        "What is the boiling point of water?",
        model="gemma:2b",  # Use the smallest model directly
        max_tokens=30,
        temperature=0.1,
    )
    print(json.dumps(response, indent=2, default=datetime_json_serializer))

    print("\n" + "=" * 80)
    print("TEST 4: HIGH LOAD SIMULATION (SHOULD USE GEMMA:2B FOR SIMPLE QUERIES)")
    print("=" * 80)
    response = middleware.process_request(
        "List three common programming languages.",
        max_tokens=30,
        _simulate_high_load=True,  # This flag will route to gemma:2b
    )
    print(json.dumps(response, indent=2, default=datetime_json_serializer))

    print("\n" + "=" * 80)
    print("TEST 5: COMPLETE FALLBACK CHAIN (ALL MODELS FAIL)")
    print("=" * 80)
    response = middleware.process_request(
        "Tell me about artificial intelligence.",
        max_tokens=100,
        _test_force_all_models_fail=True,  # This flag will force all models to fail
    )
    print(json.dumps(response, indent=2, default=datetime_json_serializer))

    print("\n" + "=" * 80)
    print("TEST 6: COMPLEX QUERY WITH PRIMARY MODEL")
    print("=" * 80)
    response = middleware.process_request(
        "Explain quantum computing and its potential impact on cryptography in simple terms.",
        model="gemma3:4b",  # Start with primary model
        max_tokens=200,  # Larger response that might stress the model
        temperature=0.9,  # Higher temperature that might cause more variability
    )
    print(json.dumps(response, indent=2, default=datetime_json_serializer))

    print("\n" + "=" * 80)
    print("PERFORMANCE STATISTICS")
    print("=" * 80)
    stats = middleware.get_recent_performance()
    print(json.dumps(stats, indent=2))

    print("\n" + "=" * 80)
    print("MODEL USAGE STATISTICS")
    print("=" * 80)
    model_stats = middleware.get_model_usage_stats()
    print(json.dumps(model_stats, indent=2))

    print("\n" + "=" * 80)
    print("END OF DEMO")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
