"""
Enhanced RAG System with Ollama Integration

This module provides a Retrieval-Augmented Generation (RAG) system that:
1. Processes multiple document types (PDF, web pages, CSV)
2. Uses SentenceTransformer for embeddings
3. Stores documents in dual vector stores (FAISS and Chroma)
4. Uses Gemma 3 4B via Ollama for text generation
5. Provides responses with source attribution and streaming
"""

import time
import warnings
from typing import List, Dict, Any, Optional, Union
import os

# Suppress deprecation warnings for a cleaner console UI
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="USER_AGENT environment variable not set")

# Set environment variables to suppress warnings
os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"
os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)

from langchain_core.documents import Document
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Import our custom modules
from processors.document_processor import DocumentProcessor
from managers.vector_store_manager import VectorStoreManager
from models.embeddings_fixed import SentenceTransformerEmbeddings

# TODO: Task 2a - Integrate the Ollama LLM into EnhancedRAG class
# TODO: Import OllamaLLM from models.ollama_integration_fixed


class EnhancedRAG:
    """Enhanced RAG system with multiple knowledge sources, streaming, and attribution."""

    def __init__(
        self,
        model: str = "gemma3:4b",
        temperature: float = 0.0,
        streaming: bool = True,
        api_url: Optional[str] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        persist_directory: str = "chroma_db",
        debug_prompts: bool = False,
        debug_stream: bool = False,
    ):
        """
        Initialize the RAG system with document processing, vector stores, and Ollama LLM.

        Args:
            model: Ollama model name. Defaults to "gemma3:4b".
            temperature: Temperature for text generation (0.0 = deterministic).
            streaming: Whether to stream responses.
            api_url: The URL of the Ollama API. If None, uses the OLLAMA_API_URL env variable.
            chunk_size: The size of text chunks for splitting documents.
            chunk_overlap: The overlap between chunks.
            persist_directory: The directory to use for Chroma persistence.
        """
        # TODO: Task 2b - Initialize the OllamaLLM component
        # TODO: Instantiate OllamaLLM, passing the relevant parameters

        # TODO: Initialize the remaining components

        # TODO: Print initialization information

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the knowledge base.

        Args:
            documents: A list of Document objects to add.
        """
        # Process documents (split into chunks, preserve metadata)
        processed_docs = self.doc_processor.process_documents(documents)

        # Add to tracking list
        self.documents.extend(processed_docs)

        # Add to vector stores
        if not self.vector_store_manager.faiss_store:
            # First time adding documents, initialize vector stores
            self.vector_store_manager.initialize_stores(processed_docs)
        else:
            # Add to existing vector stores
            self.vector_store_manager.add_documents(processed_docs)

    def add_pdf(self, file_path: str) -> str:
        """
        Add a PDF file to the knowledge base.

        Args:
            file_path: The path to the PDF file.

        Returns:
            A message indicating the result.
        """
        documents = self.doc_processor.load_pdf(file_path)
        self.add_documents(documents)
        return f"Added PDF: {file_path} with {len(documents)} pages"

    def add_web_page(self, url: str) -> str:
        """
        Add a web page to the knowledge base.

        Args:
            url: The URL of the web page.

        Returns:
            A message indicating the result.
        """
        documents = self.doc_processor.load_web_page(url)
        self.add_documents(documents)
        return f"Added web page: {url}"

    def add_wikibook(self, url: str) -> str:
        """
        Add a WikiBook to the knowledge base with specialized processing.

        Args:
            url: The URL of the WikiBook.

        Returns:
            A message indicating the result.
        """
        documents = self.doc_processor.load_wikibook(url)
        self.add_documents(documents)
        return f"Added WikiBook: {url} with {len(documents)} sections"

    def add_csv(self, file_path: str, content_column: str) -> str:
        """
        Add a CSV file to the knowledge base.

        Args:
            file_path: The path to the CSV file.
            content_column: The name of the column containing the content to use.

        Returns:
            A message indicating the result.
        """
        documents = self.doc_processor.load_csv(file_path, content_column)
        self.add_documents(documents)
        return f"Added CSV: {file_path} with {len(documents)} entries"

    def query(
        self,
        question: str,
        vector_store: str = "faiss",
        streaming: Optional[bool] = None,
    ) -> str:
        """
        Query the system with a question.

        Args:
            question: The question to ask.
            vector_store: Which vector store to use ("faiss", "chroma", or "both").
            streaming: Whether to stream the response. If None, uses the instance default.

        Returns:
            The response with source attribution.
        """
        # TODO: Task 4 - Implement the query method
        # TODO: Handle streaming settings and special commands

        # TODO: Get retriever and create prompt template

        # TODO: Create the LangChain RetrievalQA chain

        # TODO: Implement streaming response handling

        # TODO: Implement non-streaming response handling

    def _format_source_info(self, source_documents: List[Document]) -> str:
        """
        Format source information for display.

        Args:
            source_documents: A list of Document objects used as sources.

        Returns:
            A formatted string with source information.
        """
        if not source_documents:
            return "No sources found"

        source_info = []
        seen_sources = set()

        for i, doc in enumerate(source_documents):
            metadata = doc.metadata
            source = metadata.get("source", "Unknown")

            # Create a unique identifier for this source
            source_type = metadata.get("source_type", "Unknown")
            source_id = f"{source}:{source_type}"

            # Only include each source once
            if source_id in seen_sources:
                continue
            seen_sources.add(source_id)

            # Format source information based on type
            if source_type == "pdf":
                page = metadata.get("page", "Unknown")
                source_info.append(f"[{i+1}] PDF: {source} (Page {page})")
            elif source_type == "web":
                source_info.append(f"[{i+1}] Web: {source}")
            elif source_type == "wikibook":
                section = metadata.get("section", "Unknown")
                title = metadata.get("title", "Unknown")
                source_info.append(
                    f"[{i+1}] WikiBook: {title}, Section {section} ({source})"
                )
            elif source_type == "csv":
                row = metadata.get("row", "Unknown")
                source_info.append(f"[{i+1}] CSV: {source} (Row {row})")
            else:
                source_info.append(f"[{i+1}] {source}")

        return "\n".join(source_info)

    def _format_response_with_sources(
        self, response: str, source_documents: List[Document]
    ) -> str:
        """
        Format the response with source attribution.

        Args:
            response: The response text.
            source_documents: A list of Document objects used as sources.

        Returns:
            A formatted string with the response and source information.
        """
        formatted_response = response.strip()
        formatted_sources = self._format_source_info(source_documents)

        return f"{formatted_response}\n\nSources:\n{formatted_sources}"

    def _handle_command(self, command: str) -> str:
        """
        Handle special commands starting with /.

        Args:
            command: The command string.

        Returns:
            A message indicating the result.
        """
        command = command.strip().lower()

        print("\n" + "=" * 60)
        print("COMMAND EXECUTION")
        print("=" * 60)

        if command == "/reload faiss":
            print(f"Executing command: {command}")
            result = self._reload_faiss()
            print("=" * 60)
            return result

        elif command == "/reload chroma":
            print(f"Executing command: {command}")
            result = self._reload_chroma()
            print("=" * 60)
            return result

        elif command == "/reload vectordb":
            print(f"Executing command: {command}")
            result = self._reload_all_vector_stores()
            print("=" * 60)
            return result

        else:
            print(f"Unknown command: {command}")
            print("=" * 60)
            return f"""
Unknown command: {command}

Available commands:
• /reload vectordb - Rebuild both vector stores
"""
        # Removed _reload_faiss and _reload_chroma methods

    def _reload_all_vector_stores(self) -> str:
        """
        Reload both FAISS and Chroma vector stores by re-initializing them.

        Returns:
            A message indicating the result.
        """
        start_time = time.time()
        print("\nReloading all vector stores...")

        # Reset both stores
        print("  ↳ Resetting FAISS store...")
        self.vector_store_manager.reset_faiss()
        print("  ↳ Resetting Chroma store...")
        self.vector_store_manager.reset_chroma()

        # Reinitialize with existing documents
        if self.documents:
            print(f"  ↳ Re-indexing {len(self.documents)} documents...")
            # This single call re-initializes both stores
            self.vector_store_manager.initialize_stores(self.documents)
            elapsed_time = time.time() - start_time
            return f"""
✅ ALL VECTOR STORES RELOAD COMPLETE
• Documents indexed: {len(self.documents)}
• Processing time: {elapsed_time:.2f} seconds
• Status: All vector stores ready for queries
"""
        else:
            return """
✅ ALL VECTOR STORES RESET
• No documents available to index
• Status: Empty but ready
"""

    # Removed compare_vector_stores method entirely
