from typing import List
import numpy as np
import hashlib


class SimpleEmbeddings:
    """
    A simple embeddings class that uses deterministic vectors for demonstration purposes.
    This is a fallback when sentence-transformers is not available.
    """

    def __init__(self, embedding_dim: int = 384):
        """
        Initialize the embeddings provider with a specified dimension.

        Args:
            embedding_dim: The dimension of the embedding vectors.
        """
        self.embedding_dim = embedding_dim
        print(f"SimpleEmbeddings initialized with dimension {embedding_dim}")

    def embed_documents(
        self, texts: List[str], batch_size: int = 32, show_progress: bool = True
    ) -> List[List[float]]:
        """
        Get embeddings for a list of texts.

        Args:
            texts: List of texts to embed.
            batch_size: Number of texts to process in each batch.
            show_progress: Whether to show progress information.

        Returns:
            List of embedding vectors.
        """
        print(f"Generating embeddings for {len(texts)} texts")
        embeddings = []

        # Process in batches to avoid memory issues
        for batch_start in range(0, len(texts), batch_size):
            batch_end = min(batch_start + batch_size, len(texts))
            batch = texts[batch_start:batch_end]

            if show_progress:
                print(
                    f"Processing batch {batch_start//batch_size + 1}/{(len(texts)-1)//batch_size + 1} ({batch_start+1}-{batch_end}/{len(texts)})"
                )

            batch_embeddings = []
            for i, text in enumerate(batch):
                embedding = self._generate_deterministic_embedding(text)
                batch_embeddings.append(embedding)

                # Show more granular progress for large batches
                if show_progress and batch_size > 10 and (i + 1) % 10 == 0:
                    print(f"  Processed {i+1}/{len(batch)} texts in current batch")

            embeddings.extend(batch_embeddings)

            if show_progress:
                print(f"  Completed batch with {len(batch_embeddings)} embeddings")

        print(f"Successfully generated {len(embeddings)} embeddings")
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """
        Get embedding for a single query text.

        Args:
            text: The query text to embed.

        Returns:
            Embedding vector.
        """
        return self._generate_deterministic_embedding(text)

    def _generate_deterministic_embedding(self, text: str) -> List[float]:
        """
        Generate a deterministic embedding for a text using a simple but more semantically
        aware approach than just random vectors.

        Args:
            text: The text to embed.

        Returns:
            Embedding vector.
        """
        # Store original text for debugging
        original_text = text

        # Preprocess text - normalize but preserve important patterns
        # 1. Extract and save acronyms and technical terms before lowercasing
        acronyms_and_terms = set()
        import re

        # Find uppercase acronyms (e.g., FAISS, RAG, AI)
        for match in re.finditer(r"\b[A-Z]{2,}\b", text):
            acronyms_and_terms.add(match.group(0).lower())

        # Find hyphenated terms (e.g., "FAISS - Facebook AI")
        for match in re.finditer(r"\b\w+\s*-\s*\w+", text):
            parts = re.split(r"\s*-\s*", match.group(0))
            for part in parts:
                if part.strip():
                    acronyms_and_terms.add(part.strip().lower())

        # 2. Now convert to lowercase and normalize
        text = text.lower()

        # 3. Create a version with spaces around punctuation for better tokenization
        spaced_text = re.sub(r"([^\w\s])", r" \1 ", text)

        # 4. Create a version with only alphanumeric and spaces for standard processing
        clean_text = "".join(c for c in text if c.isalnum() or c.isspace())

        # Create a simple term frequency vector based on common keywords
        # This is a very basic approach but better than pure randomness
        keywords = [
            # AI-related terms - give these higher weight for AI history queries
            "ai",
            "artificial",
            "intelligence",
            "machine",
            "learning",
            "neural",
            "network",
            "deep",
            "algorithm",
            "model",
            "data",
            "training",
            "computer",
            "turing",
            "minsky",
            "mccarthy",
            "dartmouth",
            "perceptron",
            "expert",
            "system",
            "winter",
            "symbolic",
            "connectionist",
            # Vector database and search terms
            "faiss",  # Added FAISS as a specific keyword
            "facebook",
            "similarity",
            "pinecone",
            "weaviate",
            "milvus",
            "chroma",
            "qdrant",
            "annoy",
            "hnsw",
            "ivf",
            "approximate",
            "nearest",
            "neighbor",
            "ann",
            "embedding",
            "dimension",
            "euclidean",
            "cosine",
            "distance",
            "metric",
            "index",
            # RAG-related terms
            "rag",
            "retrieval",
            "augmented",
            "generation",
            "vector",
            "database",
            "semantic",
            "search",
            "query",
            "document",
            # History-related terms
            "history",
            "past",
            "timeline",
            "evolution",
            "development",
            "origin",
            "beginning",
            "early",
            "first",
            "pioneer",
            "founder",
            "created",
            # Time-related terms
            "year",
            "decade",
            "century",
            "time",
            "period",
            "era",
            "age",
            "since",
            "when",
            "date",
            "started",
            "began",
            "created",
            "invented",
            "discovered",
            # Common question words
            "what",
            "who",
            "where",
            "when",
            "why",
            "how",
            "which",
            "whose",
            "is",
            "are",
            "does",
            "do",
        ]

        # Count occurrences of each keyword using multiple approaches
        term_freq = {}

        # Initialize all keywords to 0
        for keyword in keywords:
            term_freq[keyword] = 0

        # 1. First pass: Check for exact matches with word boundaries in clean text
        for keyword in keywords:
            # Count occurrences with word boundaries
            count = 0
            start = 0
            while True:
                start = clean_text.find(keyword, start)
                if start == -1:
                    break
                # Check if it's a whole word (surrounded by spaces or at text boundaries)
                if (start == 0 or clean_text[start - 1] == " ") and (
                    start + len(keyword) == len(clean_text)
                    or clean_text[start + len(keyword)] == " "
                ):
                    count += 1
                start += 1
            term_freq[keyword] = count

        # 2. Second pass: Check for special terms we extracted earlier
        for term in acronyms_and_terms:
            if term in keywords:
                term_freq[term] += 1  # Add weight for acronyms

        # 3. Third pass: Check for compound terms like "vector database"
        compound_terms = {
            "vector database": ["vector", "database"],
            "artificial intelligence": ["artificial", "intelligence"],
            "machine learning": ["machine", "learning"],
            "neural network": ["neural", "network"],
            "facebook ai": ["facebook", "ai"],
            "similarity search": ["similarity", "search"],
        }

        for compound, components in compound_terms.items():
            if compound in text:
                for component in components:
                    if component in keywords:
                        term_freq[component] += 1  # Add weight for compound terms

        # Create a fixed-size embedding by hashing the term frequencies
        embedding = np.zeros(self.embedding_dim, dtype=np.float32)

        # Define keyword categories with weights
        keyword_categories = {
            "ai": [
                "ai",
                "artificial",
                "intelligence",
                "machine",
                "learning",
                "neural",
                "network",
                "deep",
                "algorithm",
                "model",
                "turing",
                "minsky",
                "mccarthy",
                "dartmouth",
                "perceptron",
                "expert",
                "system",
                "winter",
                "symbolic",
                "connectionist",
            ],
            "vector_db": [  # New category for vector database terms
                "faiss",
                "facebook",
                "similarity",
                "pinecone",
                "weaviate",
                "milvus",
                "chroma",
                "qdrant",
                "annoy",
                "hnsw",
                "ivf",
                "approximate",
                "nearest",
                "neighbor",
                "ann",
                "embedding",
                "dimension",
                "euclidean",
                "cosine",
                "distance",
                "metric",
                "index",
                "vector",
                "database",
            ],
            "rag": [
                "rag",
                "retrieval",
                "augmented",
                "generation",
                "semantic",
                "search",
                "query",
                "document",
            ],
            "history": [
                "history",
                "past",
                "timeline",
                "evolution",
                "development",
                "origin",
                "beginning",
                "early",
                "first",
                "pioneer",
                "founder",
                "created",
            ],
            "time": [
                "year",
                "decade",
                "century",
                "time",
                "period",
                "era",
                "age",
                "since",
                "when",
                "date",
                "started",
                "began",
                "created",
                "invented",
                "discovered",
            ],
            "question": [
                "what",
                "who",
                "where",
                "when",
                "why",
                "how",
                "which",
                "whose",
                "is",
                "are",
                "does",
                "do",
            ],
        }

        # Category weights - give AI, vector_db and history higher weights
        category_weights = {
            "ai": 2.0,  # Higher weight for AI terms
            "vector_db": 2.5,  # Highest weight for vector database terms
            "rag": 1.0,
            "history": 1.5,  # Higher weight for history terms
            "time": 1.0,
            "question": 0.5,  # Lower weight for question words
        }

        # Apply category weights to term frequencies
        for category, terms in keyword_categories.items():
            weight = category_weights[category]
            for term in terms:
                if term in term_freq and term_freq[term] > 0:
                    # Distribute the term's influence across multiple dimensions
                    positions = [
                        (hash(term) + j * 73) % self.embedding_dim for j in range(5)
                    ]
                    for pos in positions:
                        embedding[pos] += term_freq[term] * weight * 0.1

        # Add some uniqueness based on the overall text
        hash_object = hashlib.sha256(clean_text.encode())
        hash_hex = hash_object.hexdigest()
        seed = int(hash_hex[:8], 16) % (2**32 - 1)
        np.random.seed(seed)

        # Add a small random component (5% of the vector)
        random_component = np.random.randn(self.embedding_dim).astype(np.float32) * 0.05
        embedding += random_component

        # Normalize the vector to unit length
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        # Print debug information
        print(f"Original text: '{original_text[:100]}...'")
        print(f"Processed text: '{clean_text[:100]}...'")
        print(f"Detected acronyms/terms: {acronyms_and_terms}")
        print(
            f"Top keywords: {sorted([(k, v) for k, v in term_freq.items() if v > 0], key=lambda x: x[1], reverse=True)[:10]}"
        )

        # Calculate category scores
        category_scores = {}
        for category, terms in keyword_categories.items():
            score = (
                sum(term_freq.get(term, 0) for term in terms)
                * category_weights[category]
            )
            category_scores[category] = score

        print(f"Category scores: {category_scores}")

        return embedding.tolist()
