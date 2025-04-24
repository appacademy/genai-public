# LangChain RAG System with Ollama Integration

This project implements a Retrieval-Augmented Generation (RAG) system using LangChain with Gemma 3 4B integration via Ollama. The system processes multiple document types, stores them in dual vector stores for comparison, and provides responses with proper source attribution and streaming output.

## Features

- **Local LLM Integration**: Uses Gemma 3 4B via Ollama for text generation
- **Multiple Document Sources**: Supports PDF, web pages, WikiBooks, and CSV files
- **Vector Stores**: Utilizes FAISS (in-memory) for primary querying and Chroma (persistent) for storage.
- **Source Attribution**: Provides detailed source information for all responses.
- **Streaming Responses**: Supports streaming for a better user experience.
- **Interactive CLI**: Offers a simplified command interface for interaction.

## Prerequisites

- Python 3.12
- Ollama installed and running locally
- Gemma 3 4B model pulled in Ollama (`ollama pull gemma3:4b`)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd langchain-ollama-rag
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   pip install -r requirements.txt
   ```

3. Ensure Ollama is running with the Gemma 3 4B model:
   ```bash
   ollama run gemma3:4b
   ```

## Usage

### Interactive Mode

```bash
# Run the interactive mode (default)
python app.py

# Run the demo mode specifically
python app.py demo

# Specify a custom Ollama API URL
python app.py api_url http://localhost:11434
```

The interactive mode provides a menu-driven interface with the following commands:

```
• Any natural language query (e.g., "What are the best practices for team management?")
• /reload vectordb - Rebuild both FAISS and Chroma vector stores from loaded documents
• /help            - Show this help menu
• /exit            - Exit interactive mode
```

### Programmatic Usage

To use the RAG system programmatically:

```python
from rag.enhanced_rag import EnhancedRAG

# Initialize the RAG system
rag = EnhancedRAG(streaming=True)

# Add documents
rag.add_pdf("path/to/document.pdf")
rag.add_web_page("https://example.com")
rag.add_csv("path/to/data.csv", "content_column")

# Query the system
response = rag.query("What is the answer to my question?", vector_store="faiss")
print(response)

# Note: compare_vector_stores is no longer available
```

## Project Structure

```
/
├── app.py                       # Main application entry point with CLI interface
├── .env                         # Environment variables (Ollama API URL)
├── requirements.txt             # Project dependencies
├── knowledge_transfer.md        # Detailed knowledge transfer document
├── README.md                    # This file
├── data/                        # Sample documents (PDFs, CSV)
├── chroma_db/                   # Persistent Chroma vector store data
├── models/
│   ├── __init__.py
│   ├── embeddings_fixed.py      # SentenceTransformer embeddings implementation
│   └── ollama_integration_fixed.py # Ollama LLM integration
├── processors/
│   ├── __init__.py
│   └── document_processor.py    # Document loading and processing
├── managers/
│   ├── __init__.py
│   └── vector_store_manager.py  # Vector store management (FAISS & Chroma)
├── rag/
│   ├── __init__.py
│   └── enhanced_rag.py          # Core RAG implementation
└── utils/                       # Utility functions (currently minimal)
    └── __init__.py
```

## Extending the System

Here are some ways you can extend the system:

1. **Add More Document Sources**: Implement support for additional document types
2. **Implement Hybrid Search**: Combine vector search with keyword search
3. **Add Caching**: Implement caching for embeddings and query results
4. **Create a Web Interface**: Build a simple web interface for the RAG system
5. **Implement Evaluation Metrics**: Add metrics for evaluating response quality

## License

This project is licensed under the MIT License - see the LICENSE file for details.
