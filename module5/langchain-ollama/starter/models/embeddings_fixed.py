"""
SentenceTransformer Embeddings for LangChain Integration

This module provides a LangChain-compatible wrapper for embeddings.
It implements the necessary interface for embedding documents and queries.
"""

from typing import List, Optional
import os
import re
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings


class SentenceTransformerEmbeddings(Embeddings):
    """
    LangChain-compatible wrapper for sentence-transformers library.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the SentenceTransformer model.

        Args:
            model_name: The name of the Sentence Transformer model to use.
                        Defaults to "all-MiniLM-L6-v2".
        """
        print(f"Initializing SentenceTransformer embeddings with model: {model_name}")
        try:
            # Load the SentenceTransformer model
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
            # Get embedding dimension from the model
            self.embedding_dimension = self.model.get_sentence_embedding_dimension()
            print(f"Successfully initialized SentenceTransformer model '{model_name}'")
            print(f"Embedding dimension: {self.embedding_dimension}")
        except Exception as e:
            print(f"Error initializing SentenceTransformer model '{model_name}': {e}")
            print("Please ensure the model is installed or accessible.")
            # Optionally, raise the error or handle it gracefully
            raise e

    def invoke(self, text: str) -> List[float]:
        """
        Embed a single query text using the loaded SentenceTransformer model.
        (This method is added for potential future LangChain compatibility,
         but embed_query is the standard method in the Embeddings interface).

        Args:
            text: The text to embed.

        Returns:
            An embedding vector as a list of floats.
        """
        return self.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents using the loaded SentenceTransformer model.

        Args:
            texts: A list of text strings (documents) to embed.

        Returns:
            A list of embedding vectors, where each vector is a list of floats.
        """
        print(f"Embedding {len(texts)} documents using '{self.model_name}'...")
        # Clean texts before embedding
        cleaned_texts = [self._clean_text(text) for text in texts]
        embeddings = self.model.encode(cleaned_texts, show_progress_bar=True)
        print("Document embedding complete.")
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """
        Generate an embedding for a single query text using the loaded SentenceTransformer model.

        Args:
            text: The query text to embed.

        Returns:
            An embedding vector as a list of floats.
        """
        clean_text = self._clean_text(text)
        print(f"Embedding query: {clean_text[:50]}...")
        embedding = self.model.encode(clean_text)
        print("Query embedding complete.")
        return embedding.tolist()

    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing non-ASCII characters and normalizing whitespace.

        Args:
            text: The input text string.

        Returns:
            Cleaned text string.
        """
        if not isinstance(text, str):
            text = str(text) # Ensure input is a string
        # Remove non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        # Normalize whitespace (replace multiple spaces/newlines with a single space)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

# Example usage (optional, for testing)
if __name__ == "__main__":
    try:
        print("Testing SentenceTransformerEmbeddings...")
        # Initialize with the default model
        embeddings = SentenceTransformerEmbeddings()

        # Test embedding documents
        docs = ["This is the first document.", "This is the second document."]
        doc_embeddings = embeddings.embed_documents(docs)
        print(f"\nDocument Embeddings (first 5 dims):")
        for i, emb in enumerate(doc_embeddings):
            print(f"Doc {i+1}: {emb[:5]}...")
        print(f"Dimension: {len(doc_embeddings[0])}")

        # Test embedding a query
        query = "What is the first document about?"
        query_embedding = embeddings.embed_query(query)
        print(f"\nQuery Embedding (first 5 dims): {query_embedding[:5]}...")
        print(f"Dimension: {len(query_embedding)}")

        print("\nSentenceTransformerEmbeddings test completed successfully.")

    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
