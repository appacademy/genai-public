from typing import List, Any
from .enums import ComponentType  # Relative import
from .interfaces import Embedder, Retriever, Generator  # Relative import


class FallbackStrategy:
    """Defines degradation pathways for different component types"""

    def __init__(
        self,
        embedders: List[Embedder],
        retrievers: List[Retriever],
        generators: List[Generator],
    ):
        self.fallback_chains = {
            ComponentType.EMBEDDER: embedders,
            ComponentType.RETRIEVER: retrievers,
            ComponentType.GENERATOR: generators,
        }

    def get_fallback_chain(self, component_type: ComponentType) -> List[Any]:
        """Return the ordered list of fallbacks for a component type"""
        return self.fallback_chains.get(component_type, [])
