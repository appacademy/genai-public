"""
Vector Store Manager for RAG System

This module provides functionality for managing dual vector stores (FAISS and Chroma)
for document storage and retrieval.
"""

import os
import time
import shutil
from typing import List, Dict, Any, Optional, Union
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS, Chroma


class VectorStoreManager:
    """
    Manages multiple vector stores for document retrieval.

    This class provides methods for initializing, adding documents to, and querying
    from both FAISS (in-memory) and Chroma (persistent) vector stores.
    """

    def __init__(self, embedding_model, persist_directory: str = "chroma_db"):
        """
        Initialize the vector store manager.

        Args:
            embedding_model: The embedding model to use for vector stores.
            persist_directory: The directory to use for Chroma persistence.
        """
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        self.faiss_store = None
        self.chroma_store = None

    def initialize_stores(self, documents: List[Document]) -> None:
        """
        Initialize both vector stores with the provided documents.

        Args:
            documents: A list of Document objects to index.

        Raises:
            ValueError: If the documents list is empty.
        """
        if not documents:
            raise ValueError("Cannot initialize vector stores with empty document list")

        # Initialize FAISS (in-memory only)
        self.faiss_store = FAISS.from_documents(documents, self.embedding_model)

        # Initialize Chroma (persistent)
        self.chroma_store = Chroma.from_documents(
            documents, self.embedding_model, persist_directory=self.persist_directory
        )

        # Persist Chroma to disk
        self.chroma_store.persist()

        print(f"Initialized vector stores with {len(documents)} documents")

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to both vector stores.

        Args:
            documents: A list of Document objects to add.
        """
        if not documents:
            return

        # Add to FAISS
        if self.faiss_store:
            self.faiss_store.add_documents(documents)
        else:
            self.faiss_store = FAISS.from_documents(documents, self.embedding_model)

        # Add to Chroma
        if self.chroma_store:
            self.chroma_store.add_documents(documents)
        else:
            self.chroma_store = Chroma.from_documents(
                documents,
                self.embedding_model,
                persist_directory=self.persist_directory,
            )

        # Persist Chroma to disk
        self.chroma_store.persist()

    def query_stores(self, query: str, top_k: int = 4) -> Dict[str, Any]:
        """
        Query both vector stores and return the results with timing information.

        Args:
            query: The query string.
            top_k: The number of documents to retrieve.

        Returns:
            A dictionary containing the results from both stores with timing information.
        """
        results = {}

        # Query FAISS
        if self.faiss_store:
            start_time = time.time()
            faiss_docs = self.faiss_store.similarity_search(query, k=top_k)
            faiss_time = time.time() - start_time

            results["faiss"] = {"documents": faiss_docs, "retrieval_time": faiss_time}

        # Query Chroma
        if self.chroma_store:
            start_time = time.time()
            chroma_docs = self.chroma_store.similarity_search(query, k=top_k)
            chroma_time = time.time() - start_time

            results["chroma"] = {
                "documents": chroma_docs,
                "retrieval_time": chroma_time,
            }

        return results

    def get_retriever(self, store_name: str):
        """
        Get a retriever for the specified vector store.

        Args:
            store_name: The name of the vector store ("faiss" or "chroma").

        Returns:
            A retriever for the specified vector store.

        Raises:
            ValueError: If the specified store is not available.
        """
        store_name = store_name.lower()

        if store_name == "faiss":
            if not self.faiss_store:
                raise ValueError("FAISS vector store is not initialized")
            return self.faiss_store.as_retriever(search_kwargs={"k": 4})

        elif store_name == "chroma":
            if not self.chroma_store:
                raise ValueError("Chroma vector store is not initialized")
            return self.chroma_store.as_retriever(search_kwargs={"k": 4})

        else:
            raise ValueError(f"Unknown vector store: {store_name}")

    def reset_faiss(self) -> None:
        """Reset the FAISS vector store."""
        self.faiss_store = None

    def reset_chroma(self) -> None:
        """Reset the Chroma vector store and delete the persistence directory."""
        self.chroma_store = None

        # Delete the Chroma persistence directory if it exists
        if os.path.exists(self.persist_directory):
            try:
                shutil.rmtree(self.persist_directory)
                print(f"Deleted Chroma persistence directory: {self.persist_directory}")
            except Exception as e:
                print(f"Error deleting Chroma persistence directory: {e}")
