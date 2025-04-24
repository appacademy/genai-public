# Knowledge Transfer: LangChain RAG Pipeline with Dual Vector Stores

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system using LangChain with dual vector stores. The system is designed to process multiple document types, store them in vector databases, and generate responses with source attribution. The implementation uses HuggingFace models for embeddings and text generation.

## Current State

The project has been refactored into a modular structure with the following components:

### 1. Document Processing

The `DocumentProcessor` class in `solution/processors/document_processor.py` handles loading and processing documents from various sources:

- PDF files using PyPDFLoader
- Web pages using WebBaseLoader
- WikiBooks using specialized BeautifulSoup scraping
- CSV files using CSVLoader

Each document is split into chunks with appropriate text splitters, and metadata is added for source attribution. The WikiBook scraper is particularly sophisticated, extracting structured content from WikiBooks pages and preserving the section structure.

### 2. HuggingFace Integration

The project uses custom LangChain-compatible classes for HuggingFace integration:

- `EnhancedHuggingFaceEmbeddings`: A LangChain embeddings class that uses HuggingFace for embeddings
- `EnhancedLLM`: A LangChain language model class that uses HuggingFace for text generation

These classes are defined in `solution/utils/langchain_integration.py` and use the sentence-transformers/all-MiniLM-L6-v2 model for embeddings.

### 3. Vector Store Management

The `VectorStoreManager` class in `solution/vector_stores/vector_store_manager.py` manages two vector stores:

- FAISS: An in-memory vector store for fast retrieval
- Chroma: A persistent vector store for long-term storage

The class handles initialization, document addition, and querying of both stores. It also provides methods to compare the performance of the two stores.

### 4. RAG System

The `EnhancedRAG` class in `solution/app.py` combines all components:

- Document processing and ingestion
- Vector store management
- Query processing with source attribution
- Streaming response capability
- Vector store comparison
- Interactive command-line interface

The interactive mode provides a comprehensive menu-driven interface with commands for:
- Natural language queries
- Vector store comparison
- Vector store selection
- Vector store reloading
- Running demonstrations

### 5. Data

The project uses the following data sources:

- Three WikiBooks:
  - Crowdsourcing (https://en.wikibooks.org/wiki/Crowdsourcing)
  - Communication Theory (https://en.wikibooks.org/wiki/Communication_Theory)
  - E-Commerce and E-Business (https://en.wikibooks.org/wiki/E-Commerce_and_E-Business)

- Three PDF books in the `solution/data/books` and `starter_code/data/books` directories:
  - BAGuidebook2.pdf
  - Find_Employment.pdf
  - Managing_Groups_and_Teams.pdf

- Metadata CSV file in `solution/data/metadata.csv` and `starter_code/data/metadata.csv`

## Key Features

1. **Multiple Document Types**: The system can process PDFs, web pages, WikiBooks, and CSV files.

2. **HuggingFace Integration**: Uses HuggingFace models for embeddings and text generation.

3. **Dual Vector Stores with Role Specialization**:
   - FAISS: High-Speed Query Engine for fast, real-time queries
   - Chroma: Persistent Knowledge Base for long-term storage
   
   **Retrieval Pattern Differences**:
   - FAISS tends to provide more diverse results across different document types, balancing retrieval across sources
   - Chroma prioritizes highly similar documents, often returning multiple results from the same source
   - FAISS demonstrates higher recall (retrieving a wider range of potentially relevant documents)
   - Chroma shows higher precision (results are very closely matched to the query but with lower diversity)
   - These complementary retrieval patterns make a dual vector store approach valuable for robust RAG applications

4. **Source Attribution**: Provides references to the source documents in responses, enhancing transparency.

5. **Streaming Responses**: Supports streaming for real-time output, improving user experience.

6. **Vector Store Comparison**: Allows comparison of retrieval performance between different vector stores.

7. **Interactive Command-Line Interface**: Provides a user-friendly interface for interacting with the system, with commands for querying, comparing vector stores, and managing the system.

## Technical Implementation Details

### LangChain Integration

This project is built on the LangChain framework, which provides the foundation for the entire RAG pipeline. Here's how LangChain is integrated throughout the system:

1. **Vector Stores**:
   - The system uses two LangChain vector stores:
     - `FAISS` from `langchain_community.vectorstores`: An in-memory vector store optimized for speed
     - `Chroma` from `langchain_community.vectorstores`: A persistent vector store for long-term storage
   - Both vector stores implement LangChain's vector store interface, enabling consistent querying and retrieval

2. **Document Processing**:
   - LangChain document loaders handle multiple document types:
     - `PyPDFLoader` for PDF files
     - `WebBaseLoader` for web pages
     - `CSVLoader` for CSV data
   - LangChain text splitters chunk documents for optimal retrieval:
     - `RecursiveCharacterTextSplitter` for general text
     - `MarkdownTextSplitter` for WikiBooks content with structured headings

3. **Embeddings & LLMs**:
   - Custom LangChain-compatible classes integrate with HuggingFace:
     - `EnhancedHuggingFaceEmbeddings`: Extends LangChain's embeddings interface
     - `EnhancedLLM`: Implements LangChain's language model interface
   - These classes follow LangChain's protocols while adding custom functionality

4. **RAG Architecture**:
   - The system follows LangChain's RAG pattern:
     - Documents → Embeddings → Vector Stores → Retrieval → Generation
   - LangChain retrievers (`as_retriever()`) connect vector stores to the generation pipeline
   - LangChain's callback system enables streaming responses

5. **Integration Points**:
   - `VectorStoreManager`: Manages LangChain vector stores with a unified interface
   - `DocumentProcessor`: Uses LangChain loaders and splitters for document processing
   - `EnhancedRAG`: Orchestrates the entire LangChain pipeline

This comprehensive LangChain integration enables the system to leverage the framework's modular architecture while adding custom enhancements for dual vector stores and specialized document processing.

### Document Processing

The document processing pipeline includes:

1. Loading documents from various sources
2. Adding metadata for source tracking
3. Splitting documents into chunks using appropriate text splitters
4. Preserving metadata during the splitting process

The WikiBook scraper uses BeautifulSoup to extract structured content from WikiBooks pages, including:

- Title extraction
- Main content extraction
- Removal of unwanted elements (navboxes, etc.)
- Section extraction with headings
- Fallback to standard WebBaseLoader if extraction fails

### HuggingFace Integration

The HuggingFace integration includes:

1. Custom embeddings class that uses HuggingFace for embeddings (sentence-transformers/all-MiniLM-L6-v2)
2. Custom LLM class that uses HuggingFace for text generation
3. Streaming support for real-time responses
4. Integration with the HuggingFace Hub for model access

### Vector Store Management

The vector store management includes:

1. Initialization of both FAISS and Chroma vector stores
2. Adding documents to both stores
3. Querying both stores and comparing results
4. Providing retrievers for use in the RAG pipeline

### RAG System

The RAG system combines all components:

1. Document ingestion and processing
2. Vector store management
3. Query processing with source attribution
4. Streaming response capability
5. Vector store comparison

## Usage

### Interactive Mode

The system features a comprehensive interactive command-line interface:

```bash
# Run the interactive mode (default)
cd solution  # or cd starter_code
python app.py

# Run the demo mode specifically
cd solution  # or cd starter_code
python app.py demo
```

The interactive mode provides a menu-driven interface with the following commands:

```
• Any natural language query (e.g., "What is crowdsourcing?")
• /compare <query> - Compare FAISS and Chroma for a query
• /faiss <query>   - Query using FAISS vector store
• /chroma <query>  - Query using Chroma vector store
• /reload faiss    - Rebuild the FAISS vector store
• /reload chroma   - Rebuild the Chroma vector store
• /reload vectordb - Rebuild both vector stores
• /run demo        - Run the predefined demo with examples
• /help            - Show this help menu
• /exit            - Exit interactive mode
```

This interface makes it easy to:
- Ask natural language questions
- Compare results from different vector stores
- Specify which vector store to use for a query
- Reload vector stores as needed
- Run demonstrations of the system's capabilities

### Programmatic Usage

To use the RAG system programmatically:

```python
# Import the EnhancedRAG class
from app import EnhancedRAG

# Initialize the RAG system
rag = EnhancedRAG(streaming=True)

# Add documents
rag.add_wikibook("https://en.wikibooks.org/wiki/Crowdsourcing")
rag.add_pdf("data/books/BAGuidebook2.pdf")
rag.add_csv("data/metadata.csv", "Description")

# Query the system
response = rag.query("What is crowdsourcing?", vector_store="faiss")
print(response)

# Compare vector stores
comparison = rag.compare_vector_stores("What are the benefits of crowdsourcing?")

# Use special commands for vector store management
rag.query("/reload faiss")      # Reload only the FAISS vector store
rag.query("/reload chroma")     # Reload only the Chroma vector store
rag.query("/reload vectordb")   # Reload both vector stores
```

### Special Commands

The system supports special commands that can be entered as queries:

1. **Vector Store Management**:
   - `/reload FAISS`: Clears and rebuilds the FAISS vector store with existing documents
   - `/reload Chroma`: Deletes the Chroma database directory and rebuilds it with existing documents
   - `/reload vectordb`: Reloads both FAISS and Chroma vector stores

These commands are particularly useful for:
- Ensuring consistent vector representations after adding new documents
- Clearing and rebuilding a vector store that might be corrupted
- Resetting the system when experiencing unexpected retrieval results
- Testing the performance impact of reindexing

The commands provide timing information and document counts upon completion.

## Recent Changes and Refactoring

### File Organization and Cleanup

1. **Project Structure Reorganization**: Both the `solution` and `starter_code` folders have been made completely standalone applications with all necessary files and directories:
   - Each folder now has its own `data` directory with books and metadata
   - Each folder now has its own `requirements.txt` file
   - Each folder now has its own `chroma_db` directory
   - File paths in the code have been updated to use local paths

2. **Removal of Unnecessary Files**: Removed test and debugging files that were not necessary for the core application:
   - Removed test scripts (test_app.py, simple_test.py, test_imports.py, write_test.py)
   - Removed output logs (app_output.txt, app_test_output.txt, etc.)
   - Removed simplified/developmental versions (simple_app.py)
   - Removed test-related files (test_persistence.py, test_vector_stores.py, README_TESTING.md)

3. **Documentation Updates**: Updated documentation to reflect the new project structure:
   - Updated README.md with the new project structure and usage instructions
   - Updated activity-implementing-a-langchain-pipeline.md with the new project structure
   - Updated knowledge_transfer.md (this file) with the new project structure

4. **Embedding Model Update**: The embedding model was updated from sentence-transformers/all-mpnet-base-v2 to sentence-transformers/all-MiniLM-L6-v2 for better performance and consistency with the course.

5. **Vector Store Role Specialization**: Implemented clear role specialization for the dual vector stores:
   - FAISS: Optimized as a "High-Speed Query Engine" for fast, real-time queries
   - Chroma: Optimized as a "Persistent Knowledge Base" for long-term storage

6. **Interactive Command-Line Interface**: Added a comprehensive interactive mode with:
   - Menu-driven interface with help system
   - Commands for natural language queries
   - Commands for vector store comparison
   - Commands for vector store selection
   - Commands for vector store reloading
   - Command to run demonstrations
   - Menu reprinting after each response for better usability

## Next Steps for Refactoring

1. **Improve Error Handling**: Add more robust error handling and logging throughout the codebase.

2. **Optimize Performance**: Profile the code and optimize performance bottlenecks, particularly in the document processing and vector store querying.

3. **Add Caching**: Implement caching for embeddings and query results to improve performance.

4. **Enhance Testing**: Add comprehensive unit tests and integration tests.

5. **Implement Hybrid Search**: Combine vector search with keyword search for better retrieval performance.

6. **Add Document Refreshing**: Implement a mechanism to update documents in the knowledge base when their source content changes.

7. **Improve Source Attribution**: Enhance the source attribution mechanism to provide more detailed information about the sources.

8. **Add Cross-Store Retrieval Fusion**: Create an advanced retrieval mechanism that combines results from both vector stores.

9. **Implement Parallel Processing**: Use parallel processing for document loading and processing to improve performance.

10. **Add User Interface**: Create a simple web interface for interacting with the RAG system.
