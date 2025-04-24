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
from models.ollama_integration_fixed import OllamaLLM


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
        # Set up the language model
        self.streaming = streaming
        self.callbacks = [StreamingStdOutCallbackHandler()] if streaming else None

        # Initialize with OllamaLLM
        self.llm = OllamaLLM(
            model_name=model,
            temperature=temperature,
            api_url=api_url,
            debug_prompts=debug_prompts,
            debug_stream=debug_stream,
            timeout=120,
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformerEmbeddings()

        # Set up document processing and vector stores
        self.doc_processor = DocumentProcessor(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        self.vector_store_manager = VectorStoreManager(
            embedding_model=self.embedding_model, persist_directory=persist_directory
        )

        # Track documents added to the system
        self.documents = []

        print("\n" + "=" * 60)
        print("ENHANCED RAG SYSTEM INITIALIZED")
        print("=" * 60)
        print("* Document types: PDF, WikiBook, Web pages, CSV")
        print("* Embeddings: SentenceTransformer (all-MiniLM-L6-v2)")
        print("* Vector stores: FAISS (in-memory), Chroma (persistent)")
        print(f"* LLM: Ollama ({model})")
        print("* Special commands: /reload faiss, /reload chroma, /reload vectordb")
        print("=" * 60 + "\n")

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
        # Use instance streaming setting if not specified
        use_streaming = self.streaming if streaming is None else streaming # Restore original line

        # Check for special commands
        if question.startswith("/"):
            return self._handle_command(question)

        if vector_store.lower() == "both":
            return self.compare_vector_stores(question)

        # Get the appropriate retriever
        retriever = self.vector_store_manager.get_retriever(vector_store)

        # Create a template with instructions for source attribution
        prompt_template = """
        You are a helpful assistant that provides accurate information based on the given context.
        
        Answer the question based ONLY on the following context. Be specific and detailed in your response.
        If the context doesn't contain enough information to answer the question fully, extract whatever
        relevant information you can find and acknowledge the limitations of the available information.
        
        Context:
        {context}
        
        Question: {question}
        
        Your answer should be comprehensive and directly address the question using information from the context.
        """

        # Create a proper PromptTemplate
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Create a RetrievalQA chain - use the existing LLM instance
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,  # Use the existing LLM instance
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
            callbacks=self.callbacks if use_streaming else None, 
        )

        if use_streaming:
            # --- Manual Streaming Logic ---
            print("Attempting manual streaming...") # Removed DEBUG prefix
            # 1. Retrieve documents
            retrieved_docs = retriever.get_relevant_documents(question)
            print(f"Retrieved {len(retrieved_docs)} documents for manual streaming.") # Removed DEBUG prefix
            
            # 2. Format context
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            
            # 3. Format prompt
            formatted_prompt = prompt.format(context=context, question=question)
            
            # 4. Call llm.stream directly and print chunks
            print("\n--- Streaming Response ---")
            full_streamed_response = ""
            try:
                # The base LLM.stream() seems to yield strings directly, not GenerationChunks
                for chunk_text in self.llm.stream(formatted_prompt): 
                    # chunk_text is expected to be a string here
                    print(chunk_text, end="", flush=True)
                    full_streamed_response += chunk_text
            except Exception as e:
                 print(f"\nError during manual streaming: {e}")
            print("\n--- End Streaming Response ---") # Add a newline after streaming

            # 5. Format and print sources
            formatted_sources = self._format_source_info(retrieved_docs)
            print("\n\nSources:\n")
            print(formatted_sources)
            return f"\nSources:\n{formatted_sources}" # Return sources like before
            # --- End Manual Streaming Logic ---
        else:
            # --- Original Non-Streaming Logic ---
            # Execute the chain
            chain_response = qa_chain({"query": question})
            
            # Format response with sources for non-streaming case
            full_response = self._format_response_with_sources(
                chain_response.get("result", "No response generated."), 
                chain_response["source_documents"]
            )
            return full_response
            # --- End Non-Streaming Logic ---

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
