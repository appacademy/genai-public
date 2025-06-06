import time
import logging
from functools import wraps
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Rate limiter implementation with token bucket algorithm.
    """
    
    def __init__(self, requests_per_minute: int = 60):
        """
        Initialize the rate limiter.
        
        Args:
            requests_per_minute: Maximum number of requests allowed per minute
        """
        self.requests_per_minute = requests_per_minute
        self.tokens = requests_per_minute
        self.last_refill_time = time.time()
        logger.info(f"Rate limiter initialized with {requests_per_minute} requests per minute")
    
    def _refill_tokens(self) -> None:
        """
        Refill tokens based on elapsed time.
        """
        now = time.time()
        elapsed_time = now - self.last_refill_time
        
        # Calculate how many tokens to add (based on elapsed time)
        new_tokens = elapsed_time * (self.requests_per_minute / 60.0)
        
        if new_tokens > 0:
            self.tokens = min(self.tokens + new_tokens, self.requests_per_minute)
            self.last_refill_time = now
    
    def wait_for_token(self) -> float:
        """
        Wait until a token is available.
        
        Returns:
            The amount of time waited
        """
        self._refill_tokens()
        
        if self.tokens >= 1:
            # We have enough tokens, consume one and return immediately
            self.tokens -= 1
            return 0.0
            
        # Calculate how long we need to wait to get a token
        wait_time = (1 - self.tokens) / (self.requests_per_minute / 60.0)
        
        # Sleep for the required time
        time.sleep(wait_time)
        
        # After waiting, we should have a token
        self.tokens = 0  # Reset to avoid floating point accumulation errors
        self.last_refill_time = time.time()  # Reset the refill time
        
        return wait_time
    
    def __call__(self, func: Callable) -> Callable:
        """
        Decorator to apply rate limiting to a function.
        
        Args:
            func: The function to decorate
            
        Returns:
            Rate-limited function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            wait_time = self.wait_for_token()
            if wait_time > 0:
                logger.debug(f"Rate limiter: waited {wait_time:.2f} seconds for token")
            return func(*args, **kwargs)
        return wrapper
    
    def apply_exponential_backoff(self, retry_attempt: int, max_delay: float = 60.0) -> float:
        """
        Calculate delay using exponential backoff.
        
        Args:
            retry_attempt: Current retry attempt number
            max_delay: Maximum delay in seconds
            
        Returns:
            Delay time in seconds
        """
        # Base formula: 2^n seconds where n is the retry attempt
        delay = min(2 ** retry_attempt, max_delay)
        
        # Add some jitter (±20%) to avoid thundering herd problem
        jitter = delay * 0.2 * (2 * (time.time() % 1) - 1)
        final_delay = delay + jitter
        
        return max(0, final_delay)  # Ensure we don't get a negative delay