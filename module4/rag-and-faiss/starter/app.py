import os
import glob
import json
import pickle
from typing import List, Dict, Any

from dotenv import load_dotenv
import faiss
import numpy as np

# Import our custom document utilities
from document_utils import Document, split_documents

# Import our custom clients
from ollama_client import OllamaClient
from simple_embeddings import SimpleEmbeddings

# Load environment variables
load_dotenv()
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")

# Initialize the Ollama client
ollama_client = OllamaClient(OLLAMA_API_URL)


class RAGPipeline:
    def __init__(self, docs_dir: str = "data"):
        """Initialize the RAG pipeline with the directory containing documents."""
        self.docs_dir = docs_dir
        # Use SimpleEmbeddings with 384-dimensional vectors
        self.embeddings = SimpleEmbeddings()
        self.documents = []
        self.document_chunks = []
        self.faiss_index = None
        self.doc_metadata = []
        self.doc_contents = []

    def load_documents(self) -> List[Document]:
        """Load documents from the specified directory."""
        # TODO: Task 2a - Implement Document Loading
        # TODO: Use glob to find all .txt and .md files in the data directory (self.docs_dir)

        # TODO: Process each file and create Document objects

        # TODO: Store and return the documents

    def process_documents(self) -> List[Document]:
        """Split documents into chunks for better retrieval."""
        # TODO: Task 2b - Implement Document Processing
        # TODO: Check if documents exist and show processing message

        # TODO: Process each document individually and create chunks

        # TODO: Store and return the document chunks

    def create_vector_store(self, batch_size: int = 16):
        """
        Create a FAISS index with document embeddings.

        Args:
            batch_size: Number of documents to process in each batch.
        """
        # TODO: Task 3 - Implement Vector Store Creation
        # TODO: Extract and store document information

        # TODO: Initialize FAISS index with proper dimensions

        # TODO: Process documents in batches

        # TODO: Print final status

    def save_index(self, index_path: str = "faiss_index"):
        """Save the FAISS index to disk."""
        if self.faiss_index is None:
            raise ValueError("No FAISS index to save")

        # Create directory if it doesn't exist
        os.makedirs(index_path, exist_ok=True)

        # Save the FAISS index
        faiss.write_index(self.faiss_index, os.path.join(index_path, "index.faiss"))

        # Save the metadata
        with open(os.path.join(index_path, "metadata.pkl"), "wb") as f:
            pickle.dump(
                {"metadata": self.doc_metadata, "contents": self.doc_contents}, f
            )

        print(f"Saved index and metadata to {index_path}")

    def load_index(self, index_path: str = "faiss_index"):
        """Load a previously saved FAISS index."""
        # Load the FAISS index
        self.faiss_index = faiss.read_index(os.path.join(index_path, "index.faiss"))

        # Load the metadata
        with open(os.path.join(index_path, "metadata.pkl"), "rb") as f:
            data = pickle.load(f)
            self.doc_metadata = data["metadata"]
            self.doc_contents = data["contents"]

        print(f"Loaded index with {self.faiss_index.ntotal} vectors")

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query."""
        # TODO: Task 4 - Implement Retrieval Component
        # TODO: Check if index exists and print debug information

        # TODO: Generate query embedding and perform search

        # TODO: Process search results and create result objects

        # TODO: Sort and return results

    def generate_response(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Generate a response using the LLM with retrieved context."""
        # TODO: Task 5 - Implement Response Generation
        # TODO: Retrieve relevant documents

        # TODO: Format documents into context string

        # TODO: Create prompt template with instructions

        # TODO: Generate response using Ollama

        # TODO: Return answer with source information

    def delete_index(self, index_path: str = "faiss_index"):
        """Delete the FAISS index from disk."""
        if os.path.exists(index_path):
            import shutil

            shutil.rmtree(index_path)
            print(f"Deleted index at {index_path}")
        else:
            print(f"No index found at {index_path}")

        # Reset instance variables
        self.faiss_index = None
        self.doc_metadata = []
        self.doc_contents = []


# Main execution code
if __name__ == "__main__":
    # Check Ollama API health
    ollama_client.print_health_message()

    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)
        print(
            "Created data directory. Please add document files (.txt or .md) to this directory."
        )

    # Initialize the RAG pipeline
    rag = RAGPipeline()

    # Create or load the vector store
    if os.path.exists("faiss_index"):
        print("Loading existing index...")
        rag.load_index()
    else:
        print("Creating new index...")
        rag.load_documents()
        rag.process_documents()
        rag.create_vector_store()
        rag.save_index()

    # Interactive query loop
    print(
        "\nRAG Pipeline ready! Ask questions about the documents or type 'exit' to quit."
    )
    print("Special commands:")
    print("  'list': List all documents in the data folder")
    print("  'reload': Delete and recreate the index")
    print("  'exit': Exit the program")

    while True:
        # Add a horizontal line and an extra line feed for better visual separation
        print("\n" + "-" * 63 + "\n")
        query = input("Enter your question: ")

        # Handle special commands
        if query.lower() == "exit":
            break
        elif query.lower() == "list":
            print("\nListing documents in the data folder:")
            # Look for both .txt and .md files
            txt_files = glob.glob(
                os.path.join(rag.docs_dir, "**/*.txt"), recursive=True
            )
            md_files = glob.glob(os.path.join(rag.docs_dir, "**/*.md"), recursive=True)
            files = txt_files + md_files

            if not files:
                print("No documents found in the data folder.")
            else:
                print("-" * 63)
                for file_path in files:
                    file_name = os.path.basename(file_path)
                    print(f"File: {file_name}")
                print("-" * 63)
            continue
        elif query.lower() == "reload":
            print("Deleting and recreating index...")
            rag.delete_index()
            rag.load_documents()
            rag.process_documents()
            rag.create_vector_store()
            rag.save_index()
            print("Index recreated successfully!")
            continue

        # Generate and display response
        result = rag.generate_response(query)
        print(f"\nAnswer: {result['answer']}")
        print("\nSources:")
        for i, source in enumerate(result["sources"]):
            print(f"{i+1}. {source['title']} - {source['content'][:100]}...")
