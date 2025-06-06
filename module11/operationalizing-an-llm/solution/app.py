"""
Main entry point for the LLM middleware application
"""

import os
from dotenv import load_dotenv
from middleware import LLMMiddleware

# Load environment variables
load_dotenv()

# Create middleware instance
middleware = LLMMiddleware()


def process_prompt(prompt, **kwargs):
    """Process a prompt using the middleware"""
    return middleware.process_request(prompt, **kwargs)


def get_performance_stats():
    """Get performance statistics"""
    return middleware.get_recent_performance()


def get_model_stats():
    """Get model usage statistics"""
    return middleware.get_model_usage_stats()


if __name__ == "__main__":
    # Import here to avoid circular imports
    from main import run_tests

    # Run the tests
    run_tests()
