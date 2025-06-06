"""
Retry mechanisms with exponential backoff
"""

import json
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


# Export the retry decorator for use in other modules
retry_with_exponential_backoff = retry(
    retry=retry_if_exception_type(
        (requests.exceptions.RequestException, json.JSONDecodeError)
    ),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
)
