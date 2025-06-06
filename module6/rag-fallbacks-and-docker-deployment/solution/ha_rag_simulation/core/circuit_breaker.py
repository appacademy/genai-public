import time
import logging
from .enums import ComponentType, CircuitState  # Relative import
from .status import ComponentStatus  # Relative import

logger = logging.getLogger("HighAvailabilityRAG.CircuitBreaker")  # More specific logger


class CircuitBreaker:
    """Implements the circuit breaker pattern to prevent cascading failures"""

    def __init__(
        self,
        component_type: ComponentType,
        failure_threshold: float = 0.5,
        min_samples: int = 5,
        recovery_timeout: int = 30,
    ):
        self.component_type = component_type
        self.status = ComponentStatus(component_type)
        self.state = CircuitState.CLOSED
        self.failure_threshold = failure_threshold
        self.min_samples = min_samples
        self.recovery_timeout = recovery_timeout
        self.last_state_change_time = time.time()

    def execute(self, component_func, fallback_func, *args, **kwargs):
        """Execute a function with fallback if the circuit is open"""
        total_calls = self.status.failures + self.status.successes

        # Check circuit state
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has elapsed
            if time.time() - self.last_state_change_time > self.recovery_timeout:
                logger.info(
                    f"Circuit for {self.component_type.value} transitioning to HALF_OPEN"
                )
                self.state = CircuitState.HALF_OPEN
                self.last_state_change_time = time.time()
                self.status.reset_counters()
            else:
                logger.warning(
                    f"Circuit for {self.component_type.value} is OPEN, using fallback"
                )
                return fallback_func(*args, **kwargs)

        # Try the primary function with timing
        try:
            start_time = time.time()
            result = component_func(*args, **kwargs)
            end_time = time.time()

            # Record success
            self.status.record_success((end_time - start_time) * 1000)  # convert to ms

            # If half open and successful, close the circuit
            if self.state == CircuitState.HALF_OPEN:
                logger.info(
                    f"Circuit for {self.component_type.value} recovering, closing circuit"
                )
                self.state = CircuitState.CLOSED
                self.last_state_change_time = time.time()

            return result

        except Exception as e:
            # Record failure
            self.status.record_failure()
            logger.warning(f"Component {self.component_type.value} failed: {str(e)}")

            # Check if we should open the circuit
            if (
                total_calls >= self.min_samples
                and self.status.get_failure_rate() >= self.failure_threshold
            ):
                if self.state == CircuitState.CLOSED:
                    logger.error(
                        f"Circuit for {self.component_type.value} opening due to high failure rate: {self.status.get_failure_rate():.2f}"
                    )
                    self.state = CircuitState.OPEN
                    self.last_state_change_time = time.time()

            # Use fallback
            return fallback_func(*args, **kwargs)
