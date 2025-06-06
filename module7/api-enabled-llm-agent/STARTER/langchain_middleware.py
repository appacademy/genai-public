"""
LangChain middleware for the NewsAgent application.
Implements middleware for caching, rate limiting, and error handling.
"""

import logging
import time
from typing import Dict, Any, Optional, Callable, List, Union, TypeVar, Generic, cast
from functools import wraps

from langchain_core.callbacks import CallbackManagerForChainRun
from langchain_core.runnables import RunnableConfig, Runnable, RunnablePassthrough
from langchain_core.runnables.utils import Input, Output

from cache import Cache
from rate_limiter import RateLimiter
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Type variables for generic typing
T = TypeVar("T")
U = TypeVar("U")


class CachingMiddleware(Generic[Input, Output]):
    """
    Middleware that adds caching to a LangChain runnable.

    This middleware caches the results of a runnable based on its inputs,
    reducing duplicate computations and API calls.
    """

    def __init__(
        self,
        runnable: Runnable[Input, Output],
        cache_key_fn: Optional[Callable[[Input], str]] = None,
        expiry_time: int = config.DEFAULT_CACHE_EXPIRY,
    ):
        """
        Initialize the caching middleware.

        Args:
            runnable: The runnable to add caching to
            cache_key_fn: Optional function to generate cache keys from inputs
            expiry_time: Cache expiry time in seconds (default: 1 hour)
        """
        self.runnable = runnable
        self.cache = Cache(expiry_time=expiry_time)
        self.cache_key_fn = cache_key_fn or self._default_cache_key

    def _default_cache_key(self, input_data: Input) -> str:
        """
        Generate a default cache key from the input data.

        Args:
            input_data: The input data to generate a key for

        Returns:
            A string cache key
        """
        # For dictionary inputs, create a sorted string representation
        if isinstance(input_data, dict):
            # Remove any sensitive data like API keys
            safe_input = input_data.copy()
            if "apiKey" in safe_input:
                safe_input["apiKey"] = "REDACTED"

            # Sort keys for consistent hashing
            return str(sorted(safe_input.items()))

        # For other types, use string representation
        return str(input_data)

    def invoke(
        self, input_data: Input, config: Optional[RunnableConfig] = None
    ) -> Output:
        """
        Invoke the runnable with caching.

        Args:
            input_data: The input data for the runnable
            config: Optional configuration for the runnable

        Returns:
            The output of the runnable, either from cache or freshly computed
        """
        # TODO: Implement caching logic for LangChain invocations

        # TODO: 1. Generate a cache key from the input data

        # TODO: 2. Check if a result exists in the cache

        # TODO: 3. If cached, return the cached result

        # TODO: 4. Otherwise, invoke the runnable to get a fresh result

        # TODO: 5. Cache the fresh result

        # TODO: 6. Return the result


class RateLimitingMiddleware(Generic[Input, Output]):
    """
    Middleware that adds rate limiting to a LangChain runnable.

    This middleware ensures that a runnable is not invoked more frequently
    than a specified rate limit.
    """

    def __init__(
        self,
        runnable: Runnable[Input, Output],
        requests_per_minute: int = config.REQUESTS_PER_MINUTE,
    ):
        """
        Initialize the rate limiting middleware.

        Args:
            runnable: The runnable to add rate limiting to
            requests_per_minute: Maximum number of requests per minute
        """
        self.runnable = runnable
        self.rate_limiter = RateLimiter(requests_per_minute)

    def invoke(
        self, input_data: Input, config: Optional[RunnableConfig] = None
    ) -> Output:
        """
        Invoke the runnable with rate limiting.

        Args:
            input_data: The input data for the runnable
            config: Optional configuration for the runnable

        Returns:
            The output of the runnable
        """
        # Apply rate limiting
        wait_time = self.rate_limiter.wait_for_token()
        if wait_time > 0:
            logger.info(f"Rate limit applied, waited {wait_time:.2f} seconds")

        # Invoke the runnable
        return self.runnable.invoke(input_data, config)


class RetryMiddleware(Generic[Input, Output]):
    """
    Middleware that adds retry logic to a LangChain runnable.

    This middleware automatically retries a runnable if it fails,
    with exponential backoff between retries.
    """

    def __init__(
        self,
        runnable: Runnable[Input, Output],
        max_retries: int = config.MAX_RETRIES,
        backoff_factor: float = config.BACKOFF_FACTOR,
        retry_on: Optional[List[type]] = None,
    ):
        """
        Initialize the retry middleware.

        Args:
            runnable: The runnable to add retry logic to
            max_retries: Maximum number of retry attempts
            backoff_factor: Factor to increase backoff time between retries
            retry_on: List of exception types to retry on (default: all exceptions)
        """
        self.runnable = runnable
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.retry_on = retry_on or [Exception]

    def invoke(
        self, input_data: Input, config: Optional[RunnableConfig] = None
    ) -> Output:
        """
        Invoke the runnable with retry logic.

        Args:
            input_data: The input data for the runnable
            config: Optional configuration for the runnable

        Returns:
            The output of the runnable
        """
        retries = 0
        last_exception = None

        while retries <= self.max_retries:
            try:
                if retries > 0:
                    # Calculate backoff time with exponential increase
                    backoff_time = self.backoff_factor * (2 ** (retries - 1))
                    logger.info(
                        f"Retry {retries}/{self.max_retries}, waiting {backoff_time:.2f} seconds"
                    )
                    time.sleep(backoff_time)

                # Attempt to invoke the runnable
                return self.runnable.invoke(input_data, config)

            except Exception as e:
                # Check if we should retry this exception type
                should_retry = any(
                    isinstance(e, exc_type) for exc_type in self.retry_on
                )

                if not should_retry or retries >= self.max_retries:
                    # Don't retry or out of retries
                    raise

                last_exception = e
                logger.warning(
                    f"Error in runnable (attempt {retries+1}/{self.max_retries+1}): {str(e)}"
                )
                retries += 1

        # This should not be reached due to the raise in the exception handler,
        # but added for completeness
        if last_exception:
            raise last_exception

        raise RuntimeError("Unexpected error in retry logic")


def with_resilience(
    runnable: Runnable[Input, Output],
    cache_expiry: int = config.DEFAULT_CACHE_EXPIRY,
    requests_per_minute: int = config.REQUESTS_PER_MINUTE,
    max_retries: int = config.MAX_RETRIES,
    backoff_factor: float = config.BACKOFF_FACTOR,
    cache_key_fn: Optional[Callable[[Input], str]] = None,
    retry_on: Optional[List[type]] = None,
) -> Runnable[Input, Output]:
    """
    Add resilience features (caching, rate limiting, and retry logic) to a runnable.

    Args:
        runnable: The runnable to add resilience to
        cache_expiry: Cache expiry time in seconds
        requests_per_minute: Maximum number of requests per minute
        max_retries: Maximum number of retry attempts
        backoff_factor: Factor to increase backoff time between retries
        cache_key_fn: Optional function to generate cache keys from inputs
        retry_on: List of exception types to retry on

    Returns:
        A new runnable with resilience features
    """
    # TODO: Implement the middleware composition pattern for resilience

    # TODO: Apply middleware in order: retry -> rate limiting -> caching

    # TODO: Return the composed, resilient runnable
