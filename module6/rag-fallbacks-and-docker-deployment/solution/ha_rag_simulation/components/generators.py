import time
import logging
import random
from typing import List, Dict, Any, Optional
from ..core.interfaces import Generator  # Go up one level to core

logger = logging.getLogger("HighAvailabilityRAG.Components.Generators")


class PrimaryGenerator(Generator):
    """Primary LLM generator with high quality"""

    def __init__(self, failure_rate: float = 0.1):
        self.failure_rate = failure_rate

    def generate(
        self, prompt: str, context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        # Simulate potential failures
        if random.random() < self.failure_rate:
            logger.warning("Primary generator failed")
            raise Exception("Primary generation service unavailable")

        # Simulate processing time
        time.sleep(random.uniform(0.2, 0.5))

        # Use context if available
        if context and len(context) > 0:
            context_str = ", ".join([doc["text"] for doc in context])
            response = (
                f"Based on {len(context)} documents including '{context_str[:50]}...', "
            )
            response += f"the answer to '{prompt[:30]}...' is a detailed explanation with nuanced insights."
        else:
            response = f"The answer to '{prompt[:30]}...' is a detailed explanation without reference documents."

        logger.info(f"Primary generator: Generated response for '{prompt[:20]}...'")
        return response


class FallbackGenerator(Generator):
    """Smaller LLM generator with reduced quality"""

    def __init__(self, failure_rate: float = 0.05):
        self.failure_rate = failure_rate

    def generate(
        self, prompt: str, context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        # Simulate potential failures
        if random.random() < self.failure_rate:
            logger.warning("Fallback generator failed")
            raise Exception("Fallback generation service unavailable")

        # Simulate processing time (faster than primary)
        time.sleep(random.uniform(0.1, 0.25))

        # Generate a simpler response
        if context and len(context) > 0:
            response = f"Based on {len(context)} documents, here's a basic answer to '{prompt[:30]}...'"
        else:
            response = f"Here's a basic answer to '{prompt[:30]}...' without using reference documents."

        logger.info(f"Fallback generator: Generated response for '{prompt[:20]}...'")
        return response


class TemplateGenerator(Generator):
    """Template-based generator as last resort"""

    def generate(
        self, prompt: str, context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        # No failures possible, instant response
        logger.info(f"Template generator: Generated response for '{prompt[:20]}...'")
        return (
            "I'm currently experiencing technical difficulties accessing my knowledge. "
            f"Your query was about '{prompt[:50]}...'. Please try again later or "
            "rephrase your question to something more general."
        )
