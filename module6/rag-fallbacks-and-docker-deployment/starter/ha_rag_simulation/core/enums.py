from enum import Enum


class ComponentType(Enum):
    EMBEDDER = "embedder"
    RETRIEVER = "retriever"
    GENERATOR = "generator"


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, not accepting requests
    HALF_OPEN = "half_open"  # Testing if service has recovered
