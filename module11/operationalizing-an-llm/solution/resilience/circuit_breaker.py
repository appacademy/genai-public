"""
Circuit breaker implementation to protect against API failures
"""

import inspect
import logging
from functools import wraps
from typing import Callable, Any

from circuitbreaker import circuit, CircuitBreakerError


def create_circuit_breaker(failure_threshold: int = 3, recovery_timeout: int = 30):
    """
    Implement a circuit breaker to protect against API failures

    Parameters:
    - failure_threshold: Number of failures before opening the circuit
    - recovery_timeout: Seconds to wait before trying again

    Returns:
    - A decorator function that adds circuit breaker protection
    """

    def decorator(func: Callable) -> Callable:
        # Apply the circuit breaker from the library
        @circuit(failure_threshold=failure_threshold, recovery_timeout=recovery_timeout)
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = logging.getLogger("llm_app")
            caller_info = inspect.getframeinfo(inspect.currentframe().f_back)
            request_id = kwargs.get("request_id", "unknown")

            logger.debug(
                f"Circuit breaker protecting call to {func.__name__} from {caller_info.function}",
                extra={"request_id": request_id},
            )

            try:
                return func(*args, **kwargs)
            except CircuitBreakerError as e:
                logger.warning(
                    f"Circuit open for {func.__name__}. Using fallback.",
                    extra={"request_id": request_id},
                )
                raise
            except Exception as e:
                logger.error(
                    f"Error in circuit-protected function {func.__name__}: {str(e)}",
                    extra={"request_id": request_id},
                )
                raise

        return wrapper

    return decorator
