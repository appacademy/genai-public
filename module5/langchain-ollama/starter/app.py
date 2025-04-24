"""
Main Application for LangChain RAG System with Ollama Integration

This module provides the main application interface for the RAG system,
including interactive CLI and demo functionality.
"""

import os
import sys
import time
import warnings
from typing import Optional
from dotenv import load_dotenv

# --- Suppress specific warnings ---
# Ignore FutureWarning from huggingface_hub about resume_download
warnings.filterwarnings("ignore", message="`resume_download` is deprecated", category=FutureWarning)
# Ignore UserWarning from transformers about _register_pytree_node
warnings.filterwarnings("ignore", message="torch.utils._pytree._register_pytree_node is deprecated", category=UserWarning)
# --- End warning suppression ---


# Load environment variables from .env file
load_dotenv()

# Import our custom modules
from rag.enhanced_rag import EnhancedRAG
from processors.document_processor import DocumentProcessor
from models.embeddings_fixed import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from models.ollama_integration_fixed import OllamaLLM


def run_demo(api_url: Optional[str] = None):
    """
    Run a demonstration of the EnhancedRAG system with example queries.

    Args:
        api_url: The URL of the Ollama API. If None, uses the OLLAMA_API_URL env variable.
    """
    print("\n" + "=" * 60)
    print("🚀 RUNNING ENHANCED RAG SYSTEM DEMO")
    print("=" * 60)

    # Initialize the RAG system
    rag = EnhancedRAG(streaming=True, api_url=api_url)

    print("Adding documents to the knowledge base...")

    # Add sample documents from the product_docs directory
    print("\nAdding product documentation...")

    # Add documents from the data directory
    rag.add_pdf("data/books/BAGuidebook2.pdf")
    rag.add_pdf("data/books/Find_Employment.pdf")
    rag.add_pdf("data/books/Managing_Groups_and_Teams.pdf")
    
    # Load WikiBooks from metadata.csv
    print("Loading WikiBooks from metadata.csv...")
    import csv
    with open("data/metadata.csv", "r") as f:
        reader = csv.DictReader(f)
        wikibook_count = 0
        for row in reader:
            if row["URL"] and "wikibooks.org" in row["URL"] and not row["PDF_URL"]:
                wikibook_count += 1
                print(f"Loading WikiBook {wikibook_count}: {row['Title']} from {row['URL']}")
                try:
                    result = rag.add_wikibook(row["URL"])
                    print(f"Successfully loaded WikiBook: {result}")
                except Exception as e:
                    print(f"Error loading WikiBook {row['Title']}: {e}")
        print(f"Loaded {wikibook_count} WikiBooks")

    # Test queries using the unified RAG system
    print("\nTesting queries using the RAG system...")

    queries = [
        "What are the key strategies for finding employment?", # Should hit Find_Employment.pdf
        "What is crowdsourcing?", # Should hit Crowdsourcing Wikibook
        "What are the main topics covered in the BA Guidebook?", # Should hit BAGuidebook2.pdf
        "What is e-commerce?" # Should hit E-Commerce Wikibook
    ]

    for i, query in enumerate(queries):
        print(f"\nQuery {i+1}: '{query}'")
        # Use the default query method which uses FAISS by default
        response = rag.query(query) 
        # The response formatting (including sources) is handled within rag.query
        # No need to print separately here as rag.query handles streaming output
        time.sleep(1) # Allow streaming to finish
    print("-" * 60)

    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETED")
    print("=" * 60)

    return rag


def interactive_mode(api_url: Optional[str] = None):
    """
    Run an interactive session with the EnhancedRAG system.

    Args:
        api_url: The URL of the Ollama API. If None, uses the OLLAMA_API_URL env variable.
    """
    # Declare global variables at the beginning of the function
    global pdf_vector_store, wikibook_vector_store
    
    print("Starting interactive mode...")
    print(f"API URL: {api_url}")

    # Clear the console for a fresh start
    os.system("cls" if os.name == "nt" else "clear")

    try:
        # Initialize the RAG system
        print("Initializing EnhancedRAG...")
        rag = EnhancedRAG(streaming=True, api_url=api_url)
        print("EnhancedRAG initialized successfully!")
    except Exception as e:
        print(f"Error initializing EnhancedRAG: {e}")
        import traceback

        traceback.print_exc()
        return

    # Display welcome banner
    print("\n" + "=" * 60)
    print("🤖 ENHANCED RAG SYSTEM - INTERACTIVE MODE")
    print("=" * 60)

    # Add initial documents
    print("\nInitializing with documents...")

    # Add documents from the data directory
    print("  ↳ Adding documents from the data directory...")

    rag.add_pdf("data/books/BAGuidebook2.pdf")
    rag.add_pdf("data/books/Find_Employment.pdf")
    rag.add_pdf("data/books/Managing_Groups_and_Teams.pdf")

    # Load WikiBooks from metadata.csv
    print("  ↳ Loading WikiBooks from metadata.csv...")
    import csv
    with open("data/metadata.csv", "r") as f:
        reader = csv.DictReader(f)
        wikibook_count = 0
        for row in reader:
            if row["URL"] and "wikibooks.org" in row["URL"] and not row["PDF_URL"]:
                wikibook_count += 1
                print(f"  ↳ Loading WikiBook {wikibook_count}: {row['Title']} from {row['URL']}")
                try:
                    result = rag.add_wikibook(row["URL"])
                    print(f"  ↳ Successfully loaded WikiBook: {result}")
                except Exception as e:
                    print(f"  ↳ Error loading WikiBook {row['Title']}: {e}")
        print(f"  ↳ Loaded {wikibook_count} WikiBooks")

    print("  ✓ All documents loaded successfully!")
    
    # Vector stores are initialized internally by EnhancedRAG when documents are added.
    # No need for separate initialization here.
    print("\nVector stores initialized within EnhancedRAG.")

    # Show help menu
    def show_help():
        print("\nAvailable commands:")
        print(
            '• Any natural language query (e.g., "What are the best practices for team management?")'
        )
        # Removed compare, faiss, chroma, reload faiss, reload chroma, run demo
        print("• /reload vectordb - Rebuild both vector stores")
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

        # Removed handlers for /run demo, /compare, /faiss, /chroma, /reload faiss, /reload chroma

        # Use the reload commands built into EnhancedRAG
        elif user_input.lower() == "/reload vectordb":
            print(rag._handle_command("/reload vectordb"))
            show_help()
            
        elif user_input.lower().startswith("/reload"):
            # Handle unknown reload commands
            print("\nUnknown reload command. Only '/reload vectordb' is available.")
            # Reprint menu after response
            show_help()

        else:
            # Handle natural language queries using the unified RAG system
            query_count += 1
            print(f'\nProcessing query #{query_count}: "{user_input}"')
            # Use the default query method (FAISS) from the rag instance
            rag.query(user_input) # Streaming and source printing handled internally
            time.sleep(1) # Allow streaming to finish before showing help
            show_help() # Reprint menu after response


if __name__ == "__main__":
    try:
        print("Starting application...")
        # Check for command line arguments
        api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        print(f"Using API URL: {api_url}")

        if len(sys.argv) > 1:
            if sys.argv[1] == "demo":
                # Run the demo if specifically requested
                print("Running in demo mode...")
                run_demo(api_url)
            elif sys.argv[1] == "api_url" and len(sys.argv) > 2:
                # Use custom API URL if provided
                api_url = sys.argv[2]
                print(f"Using custom API URL: {api_url}")
                interactive_mode(api_url)
            else:
                print(f"Unknown argument: {sys.argv[1]}")
                print("Usage: python app.py [demo|api_url <url>]")
        else:
            # Default to interactive mode
            print("Running in interactive mode...")
            interactive_mode(api_url)

        print("Application completed successfully!")
    except Exception as e:
        print(f"Error in main application: {e}")
        import traceback

        traceback.print_exc()
