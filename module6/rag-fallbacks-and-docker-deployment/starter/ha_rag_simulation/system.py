import logging
from typing import List, Dict, Any, Optional

# Import core components
from .core.enums import ComponentType
from .core.circuit_breaker import CircuitBreaker
from .core.strategy import FallbackStrategy

# Import simulated component implementations
from .components.embedders import PrimaryEmbedder, SecondaryEmbedder, CachedEmbedder
from .components.retrievers import PrimaryRetriever, ReducedRetriever, NoRetriever
from .components.generators import (
    PrimaryGenerator,
    FallbackGenerator,
    TemplateGenerator,
)

logger = logging.getLogger("HighAvailabilityRAG.System")


class HighAvailabilityRAG:
    """Main class orchestrating the RAG system with fallbacks and monitoring"""

    def __init__(self):
        # Initialize all components
        self.embedders = [
            PrimaryEmbedder(failure_rate=0.3),  # High failure rate for testing
            SecondaryEmbedder(failure_rate=0.15),
            CachedEmbedder(),
        ]

        self.retrievers = [
            PrimaryRetriever(failure_rate=0.3),  # High failure rate for testing
            ReducedRetriever(failure_rate=0.15),
            NoRetriever(),
        ]

        self.generators = [
            PrimaryGenerator(failure_rate=0.3),  # High failure rate for testing
            FallbackGenerator(failure_rate=0.15),
            TemplateGenerator(),
        ]

        # Create fallback strategy
        self.fallback_strategy = FallbackStrategy(
            embedders=self.embedders,
            retrievers=self.retrievers,
            generators=self.generators,
        )

        # Initialize circuit breakers
        self.embedding_cb = CircuitBreaker(
            component_type=ComponentType.EMBEDDER,
            failure_threshold=0.4,
            min_samples=3,
            recovery_timeout=10,
        )

        self.retrieval_cb = CircuitBreaker(
            component_type=ComponentType.RETRIEVER,
            failure_threshold=0.4,
            min_samples=3,
            recovery_timeout=10,
        )

        self.generation_cb = CircuitBreaker(
            component_type=ComponentType.GENERATOR,
            failure_threshold=0.4,
            min_samples=3,
            recovery_timeout=10,
        )

    def get_embedding(self, text: str) -> List[float]:
        """Get embedding with fallbacks"""
        embedders = self.fallback_strategy.get_fallback_chain(ComponentType.EMBEDDER)
        if not embedders:
            raise ValueError("No embedding services configured")

        # Try primary embedder with fallbacks
        primary_embedder = embedders[0]

        def try_fallback_embedder(text: str) -> List[float]:
            # Find the next available embedder
            for i, embedder in enumerate(embedders[1:], 1):
                try:
                    logger.info(f"Trying fallback embedder {i}")
                    return embedder.embed(text)
                except Exception as e:
                    logger.warning(f"Fallback embedder {i} failed: {str(e)}")
                    continue

            # If all fallbacks fail, return a zero embedding
            logger.error("All embedding services failed")
            return [0.0] * embedders[0].dimension

        return self.embedding_cb.execute(
            component_func=primary_embedder.embed,
            fallback_func=try_fallback_embedder,
            text=text,
        )

    def get_relevant_documents(
        self, query_embedding: List[float], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Get relevant documents with fallbacks"""
        retrievers = self.fallback_strategy.get_fallback_chain(ComponentType.RETRIEVER)
        if not retrievers:
            return []

        # Try primary retriever with fallbacks
        primary_retriever = retrievers[0]

        def try_fallback_retriever(
            query_embedding: List[float], top_k: int
        ) -> List[Dict[str, Any]]:
            # Find the next available retriever
            for i, retriever in enumerate(retrievers[1:], 1):
                try:
                    logger.info(f"Trying fallback retriever {i}")
                    return retriever.retrieve(query_embedding, top_k)
                except Exception as e:
                    logger.warning(f"Fallback retriever {i} failed: {str(e)}")
                    continue

            # If all fallbacks fail, return empty list
            logger.error("All retrieval services failed")
            return []

        return self.retrieval_cb.execute(
            component_func=primary_retriever.retrieve,
            fallback_func=try_fallback_retriever,
            query_embedding=query_embedding,
            top_k=top_k,
        )

    def generate_response(
        self, prompt: str, context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Generate a response with fallbacks"""
        generators = self.fallback_strategy.get_fallback_chain(ComponentType.GENERATOR)
        if not generators:
            return "No generation services available"

        # Try primary generator with fallbacks
        primary_generator = generators[0]

        def try_fallback_generator(
            prompt: str, context: Optional[List[Dict[str, Any]]]
        ) -> str:
            # Find the next available generator
            for i, generator in enumerate(generators[1:], 1):
                try:
                    logger.info(f"Trying fallback generator {i}")
                    return generator.generate(prompt, context)
                except Exception as e:
                    logger.warning(f"Fallback generator {i} failed: {str(e)}")
                    continue

            # If all fallbacks fail, return error message
            logger.error("All generation services failed")
            return (
                "I'm currently unable to generate a response. Please try again later."
            )

        return self.generation_cb.execute(
            component_func=primary_generator.generate,
            fallback_func=try_fallback_generator,
            prompt=prompt,
            context=context,
        )

    def query(self, user_query: str) -> str:
        """Process a user query with built-in resilience to component failures"""
        logger.info(f"Processing query: '{user_query}'")

        try:
            # Step 1: Convert query to embedding
            query_embedding = self.get_embedding(user_query)

            # Step 2: Retrieve relevant documents
            relevant_docs = self.get_relevant_documents(query_embedding, top_k=3)

            # Step 3: Generate response
            response = self.generate_response(user_query, context=relevant_docs)

            return response
        except Exception as e:
            logger.error(f"Unhandled exception in query pipeline: {str(e)}")
            return "I encountered an unexpected error processing your query. Please try again."

    def get_system_health(self) -> Dict[str, Any]:
        """Get current health metrics for all components"""
        return {
            "embedder": {
                "state": self.embedding_cb.state.value,
                "failure_rate": self.embedding_cb.status.get_failure_rate(),
                "avg_response_time_ms": self.embedding_cb.status.get_avg_response_time(),
            },
            "retriever": {
                "state": self.retrieval_cb.state.value,
                "failure_rate": self.retrieval_cb.status.get_failure_rate(),
                "avg_response_time_ms": self.retrieval_cb.status.get_avg_response_time(),
            },
            "generator": {
                "state": self.generation_cb.state.value,
                "failure_rate": self.generation_cb.status.get_failure_rate(),
                "avg_response_time_ms": self.generation_cb.status.get_avg_response_time(),
            },
        }
