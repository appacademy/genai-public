import time
import logging
import random
from typing import List, Dict, Any
from ..core.interfaces import Retriever  # Go up one level to core

logger = logging.getLogger("HighAvailabilityRAG.Components.Retrievers")


class PrimaryRetriever(Retriever):
    """Primary retrieval service with high-quality results"""

    def __init__(self, failure_rate: float = 0.1):
        self.failure_rate = failure_rate
        # Simulate a document store
        self.documents = [
            {
                "id": i,
                "text": f"Document {i} with detailed information",
                "metadata": {"quality": "high"},
            }
            for i in range(20)
        ]

    def retrieve(
        self, query_embedding: List[float], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        # Simulate potential failures
        if random.random() < self.failure_rate:
            logger.warning("Primary retriever failed")
            raise Exception("Primary retrieval service unavailable")

        # Simulate processing time
        time.sleep(random.uniform(0.1, 0.3))

        # Return random documents (in real system would use embedding similarity)
        results = random.sample(self.documents, min(top_k, len(self.documents)))

        logger.info(f"Primary retriever: Retrieved {len(results)} documents")
        return results


class ReducedRetriever(Retriever):
    """Reduced retrieval service with fewer results"""

    def __init__(self, failure_rate: float = 0.05):
        self.failure_rate = failure_rate
        # Simulate a document store
        self.documents = [
            {
                "id": i,
                "text": f"Document {i} with basic information",
                "metadata": {"quality": "medium"},
            }
            for i in range(10)
        ]

    def retrieve(
        self, query_embedding: List[float], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        # Simulate potential failures
        if random.random() < self.failure_rate:
            logger.warning("Reduced retriever failed")
            raise Exception("Reduced retrieval service unavailable")

        # Simulate processing time
        time.sleep(random.uniform(0.05, 0.15))

        # Return fewer documents
        max_docs = min(top_k, min(2, len(self.documents)))
        results = random.sample(self.documents, max_docs)

        logger.info(f"Reduced retriever: Retrieved {len(results)} documents")
        return results


class NoRetriever(Retriever):
    """Fallback that returns no documents"""

    def retrieve(
        self, query_embedding: List[float], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        logger.info("NoRetriever: No documents retrieved")
        return []
