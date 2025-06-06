from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class Embedder(ABC):
    """Abstract base class for text embedding services"""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Convert text to embedding vector"""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return embedding dimension"""
        pass


class Retriever(ABC):
    """Abstract base class for vector database retrieval"""

    @abstractmethod
    def retrieve(
        self, query_embedding: List[float], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents based on embedding similarity"""
        pass


class Generator(ABC):
    """Abstract base class for text generation"""

    @abstractmethod
    def generate(
        self, prompt: str, context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Generate text based on prompt and optional context"""
        pass
