"""
Enhanced RAG System with LangChain Integration

This application implements a RAG (Retrieval-Augmented Generation) system that:
1. Processes multiple document types (PDF, web pages, CSV)
2. Uses HuggingFace models for embeddings
3. Stores documents in dual vector stores (FAISS and Chroma)
4. Provides responses with source attribution and streaming
5. Includes special commands for vector store management

NOTE: This version uses a placeholder LLM implementation that doesn't require an API token.
      In a follow-up activity, this will be replaced with Gemma 3 via Ollama.
"""

import time
import warnings
from typing import List, Dict, Any, Optional
import os
import shutil

# Suppress deprecation warnings for a cleaner console UI
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="USER_AGENT environment variable not set")
warnings.filterwarnings("ignore", message="The class `HuggingFaceHub` was deprecated")
warnings.filterwarnings(
    "ignore",
    message="Default values for EnhancedHuggingFaceEmbeddings.model_name were deprecated",
)

# Set environment variables to suppress warnings
os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"
os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)
from langchain_core.documents import Document
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS, Chroma

# Import our custom modules
from processors.document_processor import DocumentProcessor
from vector_stores.vector_store_manager import VectorStoreManager
from utils.langchain_integration import (
    EnhancedHuggingFaceEmbeddings,
    EnhancedLLM,
)


class EnhancedRAG:
    """Enhanced RAG system with multiple knowledge sources, streaming, and attribution."""

    def __init__(
        self,
        model: str = "placeholder-model",
        temperature: float = 0.0,
        streaming: bool = True,
    ):
        """
        Initialize the RAG system with document processing, vector stores, and a placeholder LLM.

        Args:
            model: Model name (placeholder for future Gemma 3 integration)
            temperature: Temperature for text generation (0.0 = deterministic)
            streaming: Whether to stream responses
        """
        # Set up the language model (placeholder implementation)
        self.streaming = streaming
        self.callbacks = [StreamingStdOutCallbackHandler()] if streaming else None
        self.llm = EnhancedLLM(model_name=model, temperature=temperature)

        # Set up document processing and vector stores
        self.doc_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager(
            embedding_model=EnhancedHuggingFaceEmbeddings()
        )

        # Track documents added to the system
        self.documents = []

        print("\n" + "=" * 60)
        print("📚 ENHANCED RAG SYSTEM INITIALIZED")
        print("=" * 60)
        print("• Document types: PDF, WikiBook, Web pages, CSV")
        print("• Vector stores: FAISS (in-memory), Chroma (persistent)")
        print("• Special commands: /reload FAISS, /reload Chroma, /reload vectordb")
        print("=" * 60 + "\n")

    def add_documents(self, documents: List[Document]):
        """Add documents to the knowledge base."""
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

    def add_pdf(self, file_path: str):
        """Add a PDF file to the knowledge base."""
        documents = self.doc_processor.load_pdf(file_path)
        self.add_documents(documents)
        return f"Added PDF: {file_path} with {len(documents)} pages"

    def add_web_page(self, url: str):
        """Add a web page to the knowledge base."""
        documents = self.doc_processor.load_web_page(url)
        self.add_documents(documents)
        return f"Added web page: {url}"

    def add_wikibook(self, url: str):
        """Add a WikiBook to the knowledge base with specialized processing."""
        documents = self.doc_processor.load_wikibook(url)
        self.add_documents(documents)
        return f"Added WikiBook: {url} with {len(documents)} sections"

    def add_csv(self, file_path: str, content_column: str):
        """Add a CSV file to the knowledge base."""
        documents = self.doc_processor.load_csv(file_path, content_column)
        self.add_documents(documents)
        return f"Added CSV: {file_path} with {len(documents)} entries"

    def query(
        self, question: str, vector_store: str = "faiss", streaming: bool = True
    ) -> str:
        """
        Query the system with a question.

        Args:
            question: The question to ask
            vector_store: Which vector store to use ("faiss", "chroma", or "both")
            streaming: Whether to stream the response

        Returns:
            The response with source attribution
        """
        # Check for special commands
        if question.startswith("/"):
            return self._handle_command(question)

        if vector_store.lower() == "both":
            return self.compare_vector_stores(question)

        # Get the appropriate retriever
        retriever = self.vector_store_manager.get_retriever(vector_store)

        # Create a template with instructions for source attribution
        prompt_template = """
        Answer the question based only on the following context. If you don't know the answer, 
        just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Question: {question}
        """

        # Create a proper PromptTemplate
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Create a RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=EnhancedLLM(
                model_name=self.llm.model_name, temperature=self.llm.temperature
            ),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        # Execute the chain
        chain_response = qa_chain({"query": question})

        # If streaming, we need to handle source documents separately
        if streaming:
            print("\n\nSources:\n")
            formatted_sources = self._format_source_info(
                chain_response["source_documents"]
            )
            print(formatted_sources)
            return formatted_sources
        else:
            # Format response with sources
            full_response = self._format_response_with_sources(
                chain_response["result"], chain_response["source_documents"]
            )
            return full_response

    def _format_source_info(self, source_documents: List[Document]) -> str:
        """Format source information for display."""
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

    def _format_response_with_sources(self, response, source_documents) -> str:
        """Format the response with source attribution."""
        formatted_response = response.strip()
        formatted_sources = self._format_source_info(source_documents)

        return f"{formatted_response}\n\nSources:\n{formatted_sources}"

    def _handle_command(self, command: str) -> str:
        """Handle special commands starting with /."""
        command = command.strip().lower()

        print("\n" + "=" * 60)
        print("🔧 COMMAND EXECUTION")
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
            print(f"❌ Unknown command: {command}")
            print("=" * 60)
            return f"""
Unknown command: {command}

Available commands:
• /reload FAISS    - Rebuild the FAISS vector store
• /reload Chroma   - Rebuild the Chroma vector store
• /reload vectordb - Rebuild both vector stores
"""

    def _reload_faiss(self) -> str:
        """Reload the FAISS vector store."""
        start_time = time.time()
        print("\n🔄 Reloading FAISS vector store...")

        # Reset the FAISS store
        print("  ↳ Resetting FAISS store...")
        self.vector_store_manager.faiss_store = None

        # Reinitialize with existing documents
        if self.documents:
            print(f"  ↳ Re-indexing {len(self.documents)} documents in FAISS...")
            self.vector_store_manager.faiss_store = FAISS.from_documents(
                self.documents, self.vector_store_manager.embedding_model
            )
            elapsed_time = time.time() - start_time
            return f"""
✅ FAISS Vector Store Reload Complete
• Documents indexed: {len(self.documents)}
• Processing time: {elapsed_time:.2f} seconds
• Status: Ready for queries
"""
        else:
            return """
✅ FAISS Vector Store Reset
• No documents available to index
• Status: Empty but ready
"""

    def _reload_chroma(self) -> str:
        """Reload the Chroma vector store."""
        import shutil
        import os

        start_time = time.time()
        print("\n🔄 Reloading Chroma vector store...")

        # Get the persist directory
        persist_dir = self.vector_store_manager.persist_directory

        # Delete the existing Chroma database if it exists
        if os.path.exists(persist_dir):
            print(f"  ↳ Removing existing Chroma database at {persist_dir}...")
            try:
                shutil.rmtree(persist_dir)
            except PermissionError:
                print(
                    f"  ⚠️ Could not remove Chroma database - it may be in use by another process"
                )
                print(f"  ↳ Continuing with reset operation...")

        # Reset the Chroma store
        print("  ↳ Resetting Chroma store...")
        self.vector_store_manager.chroma_store = None

        # Reinitialize with existing documents
        if self.documents:
            print(f"  ↳ Re-indexing {len(self.documents)} documents in Chroma...")
            self.vector_store_manager.chroma_store = Chroma.from_documents(
                self.documents,
                self.vector_store_manager.embedding_model,
                persist_directory=persist_dir,
            )
            elapsed_time = time.time() - start_time
            return f"""
✅ Chroma Vector Store Reload Complete
• Documents indexed: {len(self.documents)}
• Processing time: {elapsed_time:.2f} seconds
• Persistence directory: {persist_dir}
• Status: Ready for queries
"""
        else:
            return """
✅ Chroma Vector Store Reset
• No documents available to index
• Persistence directory cleared
• Status: Empty but ready
"""

    def _reload_all_vector_stores(self) -> str:
        """Reload both FAISS and Chroma vector stores."""
        start_time = time.time()
        print("\n🔄 Reloading all vector stores...")

        # Reload FAISS
        print("\n  ↳ Reloading FAISS vector store...")
        faiss_result = self._reload_faiss()

        # Reload Chroma
        print("\n  ↳ Reloading Chroma vector store...")
        chroma_result = self._reload_chroma()

        elapsed_time = time.time() - start_time

        return f"""
✅ ALL VECTOR STORES RELOAD COMPLETE
• Total processing time: {elapsed_time:.2f} seconds
• FAISS: Successfully reloaded with {len(self.documents)} documents
• Chroma: Successfully reloaded with {len(self.documents)} documents
• Status: All vector stores ready for queries
"""

    def compare_vector_stores(self, question: str) -> Dict[str, Any]:
        """Compare results from different vector stores."""
        print("\n" + "=" * 60)
        print("🔍 VECTOR STORE COMPARISON")
        print("=" * 60)
        print(f"Query: '{question}'")

        start_time = time.time()
        print("\n  ↳ Retrieving documents from both vector stores...")

        # Get results from both vector stores
        results = self.vector_store_manager.query_stores(question)

        # Get answers using both stores
        faiss_answer = None
        chroma_answer = None

        # Non-streaming for comparison
        non_streaming_llm = EnhancedLLM(
            model_name=self.llm.model_name, temperature=self.llm.temperature
        )

        # Create a template
        prompt_template = """
        Answer the question based only on the following context. If you don't know the answer, 
        just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Question: {question}
        """

        # Create a proper PromptTemplate
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # Process FAISS results
        if "faiss" in results:
            faiss_time = results["faiss"]["retrieval_time"]
            faiss_docs = results["faiss"]["documents"]
            print(
                f"\n  ↳ FAISS retrieved {len(faiss_docs)} documents in {faiss_time:.4f}s"
            )

            faiss_context = "\n\n".join([doc.page_content for doc in faiss_docs])

            # Get answer from LLM
            print("  ↳ Generating answer from FAISS results...")
            faiss_response = non_streaming_llm.invoke(
                prompt.format(context=faiss_context, question=question)
            )
            faiss_answer = faiss_response

        # Process Chroma results
        if "chroma" in results:
            chroma_time = results["chroma"]["retrieval_time"]
            chroma_docs = results["chroma"]["documents"]
            print(
                f"\n  ↳ Chroma retrieved {len(chroma_docs)} documents in {chroma_time:.4f}s"
            )

            chroma_context = "\n\n".join([doc.page_content for doc in chroma_docs])

            # Get answer from LLM
            print("  ↳ Generating answer from Chroma results...")
            chroma_response = non_streaming_llm.invoke(
                prompt.format(context=chroma_context, question=question)
            )
            chroma_answer = chroma_response

        # Calculate total time
        total_time = time.time() - start_time

        # Compile comparison results
        comparison = {
            "question": question,
            "total_time": total_time,
            "faiss": {
                "retrieval_time": results.get("faiss", {}).get("retrieval_time"),
                "documents": [
                    doc.page_content[:100] + "..."
                    for doc in results.get("faiss", {}).get("documents", [])
                ],
                "answer": faiss_answer,
            },
            "chroma": {
                "retrieval_time": results.get("chroma", {}).get("retrieval_time"),
                "documents": [
                    doc.page_content[:100] + "..."
                    for doc in results.get("chroma", {}).get("documents", [])
                ],
                "answer": chroma_answer,
            },
        }

        # Format for display
        print("\n" + "=" * 60)
        print("📊 COMPARISON RESULTS")
        print("=" * 60)

        # FAISS results
        faiss_time = comparison["faiss"]["retrieval_time"]
        print("\n📈 FAISS:")
        print(f"• Retrieval time: {faiss_time:.4f} seconds")
        print(f"• Documents: {len(comparison['faiss']['documents'])}")
        print(f"• Answer: {comparison['faiss']['answer']}")

        # Chroma results
        chroma_time = comparison["chroma"]["retrieval_time"]
        print("\n📈 Chroma:")
        print(f"• Retrieval time: {chroma_time:.4f} seconds")
        print(f"• Documents: {len(comparison['chroma']['documents'])}")
        print(f"• Answer: {comparison['chroma']['answer']}")

        # Performance comparison
        print("\n⚡ Performance:")
        print(f"• Total comparison time: {total_time:.4f} seconds")
        if faiss_time < chroma_time:
            speedup = chroma_time / faiss_time
            print(f"• 🏆 FAISS was {speedup:.2f}x faster than Chroma")
        else:
            speedup = faiss_time / chroma_time
            print(f"• 🏆 Chroma was {speedup:.2f}x faster than FAISS")

        print("=" * 60)

        return comparison


def run_demo():
    """Run a demonstration of the EnhancedRAG system with example queries."""
    print("\n" + "=" * 60)
    print("🚀 RUNNING ENHANCED RAG SYSTEM DEMO")
    print("=" * 60)

    # Initialize the RAG system
    rag = EnhancedRAG(streaming=True)

    print("Adding documents to the knowledge base...")

    # Add the WikiBooks
    print("\nAdding WikiBooks...")
    rag.add_wikibook("https://en.wikibooks.org/wiki/Crowdsourcing")
    rag.add_wikibook("https://en.wikibooks.org/wiki/Communication_Theory")
    rag.add_wikibook("https://en.wikibooks.org/wiki/E-Commerce_and_E-Business")

    # Add the PDF books
    print("\nAdding PDF books...")
    rag.add_pdf("data/books/BAGuidebook2.pdf")
    rag.add_pdf("data/books/Find_Employment.pdf")
    rag.add_pdf("data/books/Managing_Groups_and_Teams.pdf")

    # Add the metadata CSV
    print("\nAdding metadata...")
    rag.add_csv("data/metadata.csv", "Description")

    # Test query with streaming
    print("\nQuerying with FAISS (streaming):")
    rag.query("What is crowdsourcing?", vector_store="faiss")

    # Test query with Chroma
    print("\nQuerying with Chroma (streaming):")
    rag.query("Explain the basics of communication theory.", vector_store="chroma")

    # Compare vector stores
    print("\nComparing vector stores:")
    rag.compare_vector_stores("What are the key aspects of e-commerce?")

    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETED")
    print("=" * 60)

    return rag


def interactive_mode():
    """Run an interactive session with the EnhancedRAG system."""
    import os

    # Clear the console for a fresh start
    os.system("cls" if os.name == "nt" else "clear")

    # Initialize the RAG system
    rag = EnhancedRAG(streaming=True)

    # Display welcome banner
    print("\n" + "=" * 60)
    print("🤖 ENHANCED RAG SYSTEM - INTERACTIVE MODE")
    print("=" * 60)

    # Add initial documents
    print("\nInitializing with documents...")

    # Add WikiBooks
    print("  ↳ Adding WikiBooks...")
    rag.add_wikibook("https://en.wikibooks.org/wiki/Crowdsourcing")
    rag.add_wikibook("https://en.wikibooks.org/wiki/Communication_Theory")
    rag.add_wikibook("https://en.wikibooks.org/wiki/E-Commerce_and_E-Business")

    # Add PDF books
    print("  ↳ Adding PDF books...")
    rag.add_pdf("data/books/BAGuidebook2.pdf")
    rag.add_pdf("data/books/Find_Employment.pdf")
    rag.add_pdf("data/books/Managing_Groups_and_Teams.pdf")

    # Add metadata CSV
    print("  ↳ Adding metadata...")
    rag.add_csv("data/metadata.csv", "Description")

    print("  ✓ All documents loaded successfully!")

    # Show help menu
    def show_help():
        print("\nAvailable commands:")
        print('• Any natural language query (e.g., "What is crowdsourcing?")')
        print("• /compare <query> - Compare FAISS and Chroma for a query")
        print("• /faiss <query>   - Query using FAISS vector store")
        print("• /chroma <query>  - Query using Chroma vector store")
        print("• /reload faiss    - Rebuild the FAISS vector store")
        print("• /reload chroma   - Rebuild the Chroma vector store")
        print("• /reload vectordb - Rebuild both vector stores")
        print("• /run demo        - Run the predefined demo with examples")
        print("• /help            - Show this help menu")
        print("• /exit            - Exit interactive mode")

    show_help()

    # Query counter for session stats
    query_count = 0

    # Main interaction loop
    while True:
        print("\n" + "-" * 60)
        user_input = input("Enter your query or command: ")
        print("-" * 60)

        # Process commands
        if user_input.lower() == "/exit":
            print("\n👋 Thank you for using the Enhanced RAG System!")
            print(f"📊 Session summary: {query_count} queries processed")
            break

        elif user_input.lower() == "/help":
            show_help()

        elif user_input.lower() == "/run demo":
            print("\nRunning demo mode...")
            # Create a new RAG instance for the demo to avoid interference
            run_demo()
            print("\nReturning to interactive mode...")
            show_help()

        elif user_input.lower().startswith("/compare "):
            # Handle compare command
            query = user_input[9:].strip()  # Extract query after "/compare "
            if query:
                query_count += 1
                print(f'\nProcessing comparison query #{query_count}: "{query}"')
                rag.compare_vector_stores(query)
                # Reprint menu after response
                show_help()
            else:
                print("\n❌ Please provide a query after /compare")

        elif user_input.lower().startswith("/faiss "):
            # Handle FAISS query command
            query = user_input[7:].strip()  # Extract query after "/faiss "
            if query:
                query_count += 1
                print(f'\nProcessing FAISS query #{query_count}: "{query}"')
                rag.query(query, vector_store="faiss")
                # Reprint menu after response
                show_help()
            else:
                print("\n❌ Please provide a query after /faiss")

        elif user_input.lower().startswith("/chroma "):
            # Handle Chroma query command
            query = user_input[8:].strip()  # Extract query after "/chroma "
            if query:
                query_count += 1
                print(f'\nProcessing Chroma query #{query_count}: "{query}"')
                rag.query(query, vector_store="chroma")
                # Reprint menu after response
                show_help()
            else:
                print("\n❌ Please provide a query after /chroma")

        elif user_input.lower().startswith("/reload"):
            # Handle reload commands
            result = rag.query(user_input)
            print(result)
            # Reprint menu after response
            show_help()

        else:
            # Handle natural language queries (default to FAISS)
            query_count += 1
            print(f'\nProcessing query #{query_count}: "{user_input}"')
            rag.query(user_input, vector_store="faiss")
            # Reprint menu after response
            show_help()


# Example usage
if __name__ == "__main__":
    import sys

    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Run the demo if specifically requested
        run_demo()
    else:
        # Default to interactive mode
        interactive_mode()
