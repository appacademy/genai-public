import time
import logging
import random
import numpy as np
from typing import List
from ..core.interfaces import Embedder  # Go up one level to core

logger = logging.getLogger("HighAvailabilityRAG.Components.Embedders")


class PrimaryEmbedder(Embedder):
    """Primary embedding service (simulated)"""

    def __init__(self, failure_rate: float = 0.1):
        self.failure_rate = failure_rate

    def embed(self, text: str) -> List[float]:
        # Simulate potential failures
        if random.random() < self.failure_rate:
            logger.warning("Primary embedder failed")
            raise Exception("Primary embedding service unavailable")

        # Simulate processing time
        time.sleep(random.uniform(0.05, 0.2))

        # Generate realistic embedding (normalized vector)
        embedding = np.random.normal(0, 1, self.dimension).tolist()
        norm = sum(x**2 for x in embedding) ** 0.5
        embedding = [x / norm for x in embedding]

        logger.info(f"Primary embedder: Generated embedding for '{text[:20]}...'")
        return embedding

    @property
    def dimension(self) -> int:
        return 1536


class SecondaryEmbedder(Embedder):
    """Secondary embedding service (simulated with lower quality but higher reliability)"""

    def __init__(self, failure_rate: float = 0.05):
        self.failure_rate = failure_rate

    def embed(self, text: str) -> List[float]:
        # Simulate potential failures (but fewer than primary)
        if random.random() < self.failure_rate:
            logger.warning("Secondary embedder failed")
            raise Exception("Secondary embedding service unavailable")

        # Simulate processing time (slightly slower)
        time.sleep(random.uniform(0.1, 0.3))

        # Generate realistic embedding (normalized vector) with lower dimension
        embedding = np.random.normal(0, 1, self.dimension).tolist()
        norm = sum(x**2 for x in embedding) ** 0.5
        embedding = [x / norm for x in embedding]

        logger.info(f"Secondary embedder: Generated embedding for '{text[:20]}...'")
        return embedding

    @property
    def dimension(self) -> int:
        return 768  # Lower dimension than primary


class CachedEmbedder(Embedder):
    """Cached embedding service that returns pre-computed embeddings"""

    def __init__(self):
        # Simple simulation of a cache with random embeddings
        self.cache = {}

    def embed(self, text: str) -> List[float]:
        # Use first 10 chars as cache key (simplified)
        key = text[:10]

        # Return from cache or create new cached embedding
        if key not in self.cache:
            # Generate a stable "cached" embedding
            random.seed(hash(key))
            embedding = [random.uniform(-1, 1) for _ in range(self.dimension)]
            norm = sum(x**2 for x in embedding) ** 0.5
            self.cache[key] = [x / norm for x in embedding]

        logger.info(f"Cached embedder: Retrieved embedding for '{text[:20]}...'")
        return self.cache[key]

    @property
    def dimension(self) -> int:
        return 384  # Even lower dimension for cached embeddings
