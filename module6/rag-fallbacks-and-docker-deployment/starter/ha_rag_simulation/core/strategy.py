from typing import List, Any
from .enums import ComponentType  # Relative import
from .interfaces import Embedder, Retriever, Generator  # Relative import


class FallbackStrategy:
    """Defines degradation pathways for different component types"""

    # TODO: Task 3 - Implement the `FallbackStrategy` class.

    # TODO: Task 3a - Initialize the fallback strategy with embedders, retrievers, and generators
    def __init__(
        self,
        embedders: List[Embedder],
        retrievers: List[Retriever],
        generators: List[Generator],
    ):
        # TODO: Initialize the fallback_chains dictionary with component types as keys
        # TODO: Create a dictionary with ComponentType.EMBEDDER, ComponentType.RETRIEVER, and ComponentType.GENERATOR as keys
        # TODO: Assign the respective lists (embedders, retrievers, generators) as values to each key
        self.fallback_chains = {
            # Complete this dictionary initialization with three key-value pairs
            # using ComponentType enums as keys
        }

    def get_fallback_chain(self, component_type: ComponentType) -> List[Any]:
        """Return the ordered list of fallbacks for a component type"""
        # TODO: Task 3b - Initialize the fallback strategy with embedders, retrievers, and generators

        # TODO: Return the appropriate fallback chain for the given component type
