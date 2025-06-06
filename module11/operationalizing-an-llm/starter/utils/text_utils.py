"""
Text sanitization and processing utilities
"""

import re
from typing import List, Tuple


def sanitize_text(text: str) -> str:
    """Remove potentially sensitive information from text for logging"""
    # This is a simple example - in production you might use more sophisticated
    # techniques like named entity recognition to identify sensitive data

    # Patterns to sanitize (simple examples)
    patterns: List[Tuple[str, str]] = [
        (
            r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
            "[CREDIT_CARD]",
        ),  # Credit card
        (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]"),  # Social Security Number
        (
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "[EMAIL]",
        ),  # Email
        (
            r"\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b",
            "[PHONE]",
        ),  # Phone
    ]

    sanitized = text
    for pattern, replacement in patterns:
        sanitized = re.sub(pattern, replacement, sanitized)

    return sanitized
