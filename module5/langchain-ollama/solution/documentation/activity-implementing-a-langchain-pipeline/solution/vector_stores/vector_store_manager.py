"""
Vector Store Manager Module

This module manages multiple vector stores for document retrieval:
- FAISS (in-memory vector store)
- Chroma (persistent vector store)

It provides functionality to initialize stores, add documents, query stores,
and get retrievers for use in the RAG pipeline.
"""

import time
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS, Chroma
from utils.langchain_integration import EnhancedHuggingFaceEmbeddings


class VectorStoreManager:
    """Manages multiple vector stores for document retrieval."""

    def __init__(self, embedding_model=None):
        self.embedding_model = embedding_model or EnhancedHuggingFaceEmbeddings()
        self.faiss_store = None
        self.chroma_store = None
        self.persist_directory = "chroma_db"

    def initialize_stores(self, documents: List[Document]):
        """Initialize both vector stores with the same documents."""
        if not documents:
            raise ValueError("Cannot initialize vector stores with empty document list")

        # Initialize FAISS (in-memory)
        self.faiss_store = FAISS.from_documents(documents, self.embedding_model)

        # Initialize Chroma (persistent)
        self.chroma_store = Chroma.from_documents(
            documents, self.embedding_model, persist_directory=self.persist_directory
        )
        self.chroma_store.persist()

        print(f"Initialized vector stores with {len(documents)} documents")

    def add_documents(self, documents: List[Document]):
        """Add documents to both vector stores."""
        if not documents:
            return

        # Add to FAISS
        if self.faiss_store is not None:
            self.faiss_store.add_documents(documents)
        else:
            self.faiss_store = FAISS.from_documents(documents, self.embedding_model)

        # Add to Chroma
        if self.chroma_store is not None:
            self.chroma_store.add_documents(documents)
        else:
            self.chroma_store = Chroma.from_documents(
                documents,
                self.embedding_model,
                persist_directory=self.persist_directory,
            )
            self.chroma_store.persist()

    def query_stores(self, query: str, top_k: int = 4) -> Dict[str, Any]:
        """Query both vector stores and return results."""
        results = {}

        # Query FAISS
        if self.faiss_store is not None:
            faiss_start = time.time()
            results["faiss"] = {
                "documents": self.faiss_store.similarity_search(query, k=top_k),
                "retrieval_time": time.time() - faiss_start,
            }

        # Query Chroma
        if self.chroma_store is not None:
            chroma_start = time.time()
            results["chroma"] = {
                "documents": self.chroma_store.similarity_search(query, k=top_k),
                "retrieval_time": time.time() - chroma_start,
            }

        return results

    def get_retriever(self, store_name: str = "faiss"):
        """Get a retriever for the specified vector store."""
        if store_name.lower() == "faiss" and self.faiss_store is not None:
            return self.faiss_store.as_retriever(search_kwargs={"k": 4})
        elif store_name.lower() == "chroma" and self.chroma_store is not None:
            return self.chroma_store.as_retriever(search_kwargs={"k": 4})
        else:
            raise ValueError(f"Vector store '{store_name}' is not available")
