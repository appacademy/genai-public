from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os


def load_documents(policy_dir="data/policies", benefits_dir="data/benefits"):
    """Load policy and benefits documents and split into chunks"""
    # Ensure directories exist
    os.makedirs(policy_dir, exist_ok=True)
    os.makedirs(benefits_dir, exist_ok=True)

    # Create loaders with improved error handling
    policy_loader = DirectoryLoader(
        policy_dir,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
            "autodetect_encoding": True,
        },
    )
    benefits_loader = DirectoryLoader(
        benefits_dir,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
            "autodetect_encoding": True,
        },
    )

    # Load documents with better error handling
    try:
        policy_docs = policy_loader.load()
        print(f"Loaded {len(policy_docs)} policy documents from {policy_dir}")
    except Exception as e:
        print(f"Error loading policy documents: {e}")
        policy_docs = []

    try:
        benefits_docs = benefits_loader.load()
        print(f"Loaded {len(benefits_docs)} benefit documents from {benefits_dir}")
    except Exception as e:
        print(f"Error loading benefit documents: {e}")
        benefits_docs = []

    # Tag documents with source and proper file names
    for doc in policy_docs:
        source_path = doc.metadata.get("source", "")
        doc.metadata["source"] = "policy"
        doc.metadata["source_file"] = os.path.basename(source_path)
        doc.metadata["full_source_path"] = source_path
        # Add document type based on filename keywords for better classification
        filename = os.path.basename(source_path).lower()
        if any(
            keyword in filename for keyword in ["pto", "vacation", "time off", "leave"]
        ):
            doc.metadata["document_type"] = "leave_policy"
        elif any(
            keyword in filename
            for keyword in ["harassment", "discrimination", "conduct"]
        ):
            doc.metadata["document_type"] = "workplace_policy"
        else:
            doc.metadata["document_type"] = "general_policy"

    for doc in benefits_docs:
        source_path = doc.metadata.get("source", "")
        doc.metadata["source"] = "benefit"
        doc.metadata["source_file"] = os.path.basename(source_path)
        doc.metadata["full_source_path"] = source_path
        # Add benefit type based on filename keywords
        filename = os.path.basename(source_path).lower()
        if any(
            keyword in filename for keyword in ["health", "medical", "dental", "vision"]
        ):
            doc.metadata["document_type"] = "health_benefits"
        elif any(keyword in filename for keyword in ["retirement", "401k", "pension"]):
            doc.metadata["document_type"] = "retirement_benefits"
        else:
            doc.metadata["document_type"] = "general_benefits"

    # Combine documents
    all_docs = policy_docs + benefits_docs

    if not all_docs:
        print("Warning: No documents were loaded. Check the data directories.")
        return []

    # Split documents with improved settings for better context retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""],
        keep_separator=True,
    )
    chunks = text_splitter.split_documents(all_docs)

    print(f"Created {len(chunks)} document chunks from {len(all_docs)} documents")
    return chunks


def create_vector_store(chunks, vector_store_path="data/vector_store"):
    """Create and save FAISS vector store from document chunks"""
    if not chunks:
        print("No document chunks provided to create vector store.")
        return None

    # Ensure vector store directory exists
    os.makedirs(vector_store_path, exist_ok=True)

    # Use sentence-transformers for embeddings (offline use)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    try:
        print(f"Creating vector store with {len(chunks)} chunks...")
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(vector_store_path)
        print(f"Vector store saved to {vector_store_path}")
        return vector_store
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None


def load_vector_store(vector_store_path="data/vector_store"):
    """Load an existing FAISS vector store"""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists(vector_store_path):
        try:
            print(f"Loading vector store from {vector_store_path}...")
            return FAISS.load_local(
                vector_store_path, embeddings, allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Error loading vector store: {e}")
            raise FileNotFoundError(
                f"Failed to load vector store from {vector_store_path}: {e}"
            )
    else:
        raise FileNotFoundError(f"Vector store not found at {vector_store_path}")
