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
        document_list = []
        # Look for both .txt and .md files
        txt_files = glob.glob(os.path.join(self.docs_dir, "**/*.txt"), recursive=True)
        md_files = glob.glob(os.path.join(self.docs_dir, "**/*.md"), recursive=True)
        files = txt_files + md_files

        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                # Create metadata based on file information
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_path)[1]
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": file_path,
                        "title": file_name,
                        "file_path": file_path,
                        "file_type": file_ext,
                        "is_markdown": file_ext.lower() == ".md",
                    },
                )
                document_list.append(doc)

        self.documents = document_list
        print(f"Loaded {len(document_list)} documents")
        return document_list

    def process_documents(self) -> List[Document]:
        """Split documents into chunks for better retrieval."""
        if not self.documents:
            print("No documents to process. Call load_documents first.")
            return []

        print(f"Processing {len(self.documents)} documents...")

        # Process documents one by one to avoid memory issues
        all_chunks = []
        for i, doc in enumerate(self.documents):
            print(
                f"Processing document {i+1}/{len(self.documents)}: {doc.metadata.get('title', 'Untitled')}"
            )

            # Split this document into chunks
            doc_chunks = split_documents(
                [doc],  # Process one document at a time
                chunk_size=1500,
                chunk_overlap=300,
                separators=[
                    "\n## ",
                    "\n### ",
                    "\n#### ",
                    "\n",
                    " ",
                    "",
                ],  # Respect markdown headings
            )

            all_chunks.extend(doc_chunks)
            print(f"  Created {len(doc_chunks)} chunks from document {i+1}")

        self.document_chunks = all_chunks
        print(f"Created {len(all_chunks)} document chunks in total")
        return all_chunks

    def create_vector_store(self, batch_size: int = 16):
        """
        Create a FAISS index with document embeddings.

        Args:
            batch_size: Number of documents to process in each batch.
        """
        if not self.document_chunks:
            raise ValueError(
                "No document chunks available. Call process_documents first."
            )

        # Store document metadata and contents
        self.doc_metadata = [doc.metadata for doc in self.document_chunks]
        self.doc_contents = [doc.page_content for doc in self.document_chunks]

        # Get all document texts
        texts = [doc.page_content for doc in self.document_chunks]
        total_docs = len(texts)

        print(f"Creating vector store for {total_docs} document chunks...")

        # Process in batches to avoid memory issues
        # First, get the embedding dimension from a single document
        sample_embedding = self.embeddings.embed_query(texts[0] if texts else "")
        dimension = len(sample_embedding)

        # Initialize FAISS index
        self.faiss_index = faiss.IndexFlatL2(dimension)
        print(f"Initialized FAISS index with dimension {dimension}")

        # Process documents in batches
        for batch_start in range(0, total_docs, batch_size):
            batch_end = min(batch_start + batch_size, total_docs)
            batch_texts = texts[batch_start:batch_end]

            print(
                f"Processing batch {batch_start//batch_size + 1}/{(total_docs-1)//batch_size + 1} ({batch_start+1}-{batch_end}/{total_docs})"
            )

            # Generate embeddings for this batch
            batch_embeddings = self.embeddings.embed_documents(
                batch_texts,
                batch_size=min(batch_size, 8),  # Use smaller internal batches
                show_progress=(
                    batch_end - batch_start > 8
                ),  # Only show progress for larger batches
            )

            # Convert to numpy array and add to index
            batch_embedding_array = np.array(batch_embeddings, dtype=np.float32)
            self.faiss_index.add(batch_embedding_array)

            print(
                f"Added {len(batch_embeddings)} vectors to index (total: {self.faiss_index.ntotal})"
            )

        print(
            f"Created FAISS index with {self.faiss_index.ntotal} vectors of dimension {dimension}"
        )

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
        if self.faiss_index is None:
            raise ValueError("No FAISS index available. Create or load an index first.")

        # Print debug information
        print(f"\nRetrieving documents for query: '{query}'")
        print(f"Index contains {self.faiss_index.ntotal} vectors")
        print(f"Metadata contains {len(self.doc_metadata)} entries")
        print(f"Content contains {len(self.doc_contents)} entries")

        # Generate embedding for the query using SimpleEmbeddings
        query_embedding = self.embeddings.embed_query(query)
        query_embedding_array = np.array([query_embedding], dtype=np.float32)

        # Perform similarity search
        distances, indices = self.faiss_index.search(query_embedding_array, top_k)

        print(f"Search returned indices: {indices[0]}")
        print(f"Search returned distances: {distances[0]}")

        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid index
                # Verify index is within bounds
                if idx < len(self.doc_contents) and idx < len(self.doc_metadata):
                    result = {
                        "content": self.doc_contents[idx],
                        "metadata": self.doc_metadata[idx],
                        "score": float(
                            distances[0][i]
                        ),  # Convert to native Python float
                    }
                    results.append(result)

                    # Print debug info about the retrieved document
                    source = self.doc_metadata[idx].get("source", "Unknown")
                    title = self.doc_metadata[idx].get("title", "Unknown")
                    content_preview = (
                        self.doc_contents[idx][:100] + "..."
                        if len(self.doc_contents[idx]) > 100
                        else self.doc_contents[idx]
                    )
                    print(
                        f"Retrieved document {i+1}: {title} (score: {distances[0][i]:.4f})"
                    )
                    print(f"  Source: {source}")
                    print(f"  Content preview: {content_preview}")
                else:
                    print(
                        f"Warning: Index {idx} is out of bounds (metadata: {len(self.doc_metadata)}, contents: {len(self.doc_contents)})"
                    )

        # Sort by relevance score (lower distance is better)
        results.sort(key=lambda x: x["score"])

        return results

    def generate_response(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Generate a response using the LLM with retrieved context."""
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(query, top_k=top_k)

        # Format documents as context string
        context_str = "\n\n".join(
            [
                f"Document {i+1} (Source: {doc['metadata'].get('title', 'Unknown')}):\n{doc['content']}"
                for i, doc in enumerate(retrieved_docs)
            ]
        )

        # Format the prompt
        prompt_template = """You are an assistant with access to the following documents:

        {context}

        These documents may contain markdown formatting. When referring to content from these documents, maintain any relevant formatting in your response.

        Using only the information from these documents, please answer the following question:
        Question: {question}

        Please keep in mind these guidelines:
        1. Provide a comprehensive answer that synthesizes information from multiple documents when available
        2. Include specific details, examples, and quotes from the documents to support your answer
        3. Structure your response in a clear, organized manner
        4. If information appears in multiple documents, combine it for a more complete answer
        5. If documents contain conflicting information, acknowledge the different perspectives
        6. Avoid drawing conclusions beyond what is explicitly stated in the documents
        7. If the information needed to answer the question is not present in the documents, please say "I don't have enough information to answer this question" instead of making up an answer

        Your goal is to provide the most helpful, accurate, and comprehensive response based solely on the provided documents.
        """

        formatted_prompt = prompt_template.replace("{context}", context_str).replace(
            "{question}", query
        )

        # Generate the answer using Ollama
        ollama_result = ollama_client.generate(formatted_prompt)
        answer = ollama_result["response"]

        # Return the answer along with source documents
        return {
            "answer": answer,
            "sources": [
                {
                    "title": doc["metadata"].get("title", "Unknown"),
                    "content": doc["content"],
                    "source": doc["metadata"].get("source", "Unknown"),
                    "score": doc["score"],
                }
                for doc in retrieved_docs
            ],
        }

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
