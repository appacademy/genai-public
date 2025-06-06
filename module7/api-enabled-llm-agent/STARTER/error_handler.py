import logging
import time
from functools import wraps
from typing import Callable, Any
import requests

logger = logging.getLogger(__name__)

# Circuit breaker states
CLOSED = 'closed'  # Normal operation
OPEN = 'open'      # Failing, don't make API calls
HALF_OPEN = 'half_open'  # Testing if API is back to normal

class CircuitBreaker:
    """
    Implementation of the circuit breaker pattern to prevent repeated calls to failing services.
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        """
        Initialize the circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening the circuit
            recovery_timeout: Time in seconds to wait before trying again
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
    
    def __call__(self, func):
        """
        Decorator to apply circuit breaker pattern to a function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == OPEN:
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    logger.info("Circuit half-open, testing service availability")
                    self.state = HALF_OPEN
                else:
                    logger.warning("Circuit open, skipping API call")
                    raise Exception("Service unavailable due to circuit breaker")
            
            try:
                result = func(*args, **kwargs)
                
                # If we were in half-open state and the call succeeded, reset the circuit
                if self.state == HALF_OPEN:
                    logger.info("Service recovered, closing circuit")
                    self.reset()
                    
                return result
                
            except Exception as e:
                self.record_failure()
                raise e
                
        return wrapper
    
    def record_failure(self):
        """Record a failure and potentially open the circuit."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CLOSED and self.failure_count >= self.failure_threshold:
            logger.warning(f"Failure threshold reached ({self.failure_count} failures), opening circuit")
            self.state = OPEN
    
    def reset(self):
        """Reset the circuit breaker to closed state."""
        self.failure_count = 0
        self.state = CLOSED

def handle_api_request(max_retries: int = 3, backoff_factor: float = 2.0):
    """
    Decorator for handling API requests with retry logic and circuit breaker.
    
    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Exponential backoff factor
        
    Returns:
        Decorated function
    """
    circuit_breaker = CircuitBreaker()
    
    def decorator(func):
        @wraps(func)
        @circuit_breaker
        def wrapper(*args, **kwargs):
            retries = 0
            
            while True:
                try:
                    return func(*args, **kwargs)
                    
                except requests.exceptions.HTTPError as e:
                    status_code = e.response.status_code
                    retries += 1
                    
                    # Handle different status codes appropriately
                    if status_code == 429:  # Too Many Requests
                        if retries <= max_retries:
                            wait_time = calculate_backoff(retries, backoff_factor)
                            logger.warning(f"Rate limit hit, retrying in {wait_time:.2f} seconds (Attempt {retries}/{max_retries})")
                            time.sleep(wait_time)
                        else:
                            logger.error(f"Rate limit hit and max retries ({max_retries}) exceeded")
                            raise
                            
                    elif status_code >= 500:  # Server errors
                        if retries <= max_retries:
                            wait_time = calculate_backoff(retries, backoff_factor)
                            logger.warning(f"Server error {status_code}, retrying in {wait_time:.2f} seconds (Attempt {retries}/{max_retries})")
                            time.sleep(wait_time)
                        else:
                            logger.error(f"Server error {status_code} and max retries ({max_retries}) exceeded")
                            raise
                            
                    elif status_code == 401:  # Unauthorized
                        logger.error("API authentication failed (401 Unauthorized)")
                        raise
                        
                    elif status_code == 403:  # Forbidden
                        logger.error("API access forbidden (403 Forbidden)")
                        raise
                        
                    elif status_code == 404:  # Not Found
                        logger.error("Resource not found (404 Not Found)")
                        raise
                        
                    else:  # Other client errors
                        logger.error(f"HTTP error {status_code}: {e}")
                        raise
                        
                except requests.exceptions.ConnectionError as e:
                    retries += 1
                    if retries <= max_retries:
                        wait_time = calculate_backoff(retries, backoff_factor)
                        logger.warning(f"Connection error, retrying in {wait_time:.2f} seconds (Attempt {retries}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Connection error and max retries ({max_retries}) exceeded")
                        raise
                        
                except requests.exceptions.Timeout as e:
                    retries += 1
                    if retries <= max_retries:
                        wait_time = calculate_backoff(retries, backoff_factor)
                        logger.warning(f"Request timed out, retrying in {wait_time:.2f} seconds (Attempt {retries}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Request timed out and max retries ({max_retries}) exceeded")
                        raise
                        
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
                    raise
                    
        return wrapper
    
    return decorator

def calculate_backoff(retry_attempt: int, backoff_factor: float) -> float:
    """
    Calculate the exponential backoff time.
    
    Args:
        retry_attempt: Current retry attempt number
        backoff_factor: Base factor for exponential calculation
        
    Returns:
        Backoff time in seconds
    """
    return backoff_factor ** retry_attempt