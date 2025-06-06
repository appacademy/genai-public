import time
from collections import deque
from .enums import ComponentType  # Relative import


class ComponentStatus:
    """Tracks the health and performance of a component"""

    def __init__(self, component_type: ComponentType):
        self.component_type = component_type
        self.response_times = deque(maxlen=100)  # Keep only recent times
        self.failures = 0
        self.successes = 0
        self.last_failure_time = None
        self.last_success_time = None

    def record_success(self, response_time_ms: float):
        """Record a successful operation"""
        self.successes += 1
        self.response_times.append(response_time_ms)
        self.last_success_time = time.time()

    def record_failure(self):
        """Record a failed operation"""
        self.failures += 1
        self.last_failure_time = time.time()

    def get_failure_rate(self) -> float:
        """Calculate the current failure rate"""
        total = self.failures + self.successes
        if total == 0:
            return 0.0
        return self.failures / total

    def get_avg_response_time(self) -> float:
        """Get the average response time over recent operations"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)

    def reset_counters(self):
        """Reset failure and success counters"""
        self.failures = 0
        self.successes = 0
