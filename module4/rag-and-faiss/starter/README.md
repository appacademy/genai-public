# RAG Implementation with FAISS and Sentence Embeddings

This project implements a Retrieval-Augmented Generation (RAG) system using FAISS as a vector database and sentence embeddings. It's designed as a learning activity for students studying Generative AI for Software Developers.

## What This Application Does

This console-based application demonstrates a complete RAG (Retrieval-Augmented Generation) pipeline:

1. **Document Processing**: The application loads text and markdown documents from the `data` directory, processes them, and splits them into manageable chunks while preserving their context and structure.

2. **Vector Embeddings**: Each document chunk is converted into a numerical vector (embedding) that captures its semantic meaning using a simple but effective embedding approach.

3. **Vector Database**: These embeddings are stored in a FAISS index, which enables efficient similarity search.

4. **Semantic Search**: When you ask a question, the application converts your query into an embedding and finds the most similar document chunks in the vector database.

5. **Context-Aware Generation**: The retrieved document chunks are used as context for a local LLM (Ollama with gemma3:4b) to generate an accurate, grounded response to your question.

This approach combines the knowledge from your documents with the language capabilities of an LLM, resulting in responses that are both relevant and factually accurate.

## Setup Instructions

### 1. Create and Activate a Virtual Environment

Create and activate a virtual environment for your project:

- **Windows (PowerShell)**:

  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  ```

- **Windows (Git Bash)**:

  ```bash
  python -m venv .venv
  source .venv/Scripts/activate
  ```

- **Mac/Linux**:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 2. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

If you encounter a "No module named 'sentence_transformers'" error, install it directly:

```bash
pip install sentence-transformers
```

### 3. Configure Environment

1. Copy the file `.env.template` into the same directory and name it `.env`:

   ```bash
   # Windows
   copy .env.template .env
   
   # Mac/Linux
   cp .env.template .env
   ```

2. If needed, update the OLLAMA_API_URL in the .env file with your own URL.

### 4. Start Ollama

1. Ensure Ollama is installed on your system. If not, download it from [ollama.ai](https://ollama.ai).

2. Start Ollama with the gemma3:4b model:

   ```bash
   ollama run gemma3:4b
   ```

## Running the Application

Run the application with:

```bash
python app.py
```

## Special Commands

When running the application, you can use these special commands:

- `list`: Lists all documents in the data folder, showing you what content is available for querying. Use this command to verify that your documents have been loaded correctly.

- `reload`: Deletes and recreates the FAISS index. This is useful when you make changes to your implementation (like modifying chunking parameters or embedding generation) and want to see their effects without restarting the application.

- `exit`: Exits the program and returns to the command line.

For any other input, the application will treat it as a question and attempt to retrieve relevant information from your documents to generate a response.

## Activity Instructions

For detailed instructions on completing the activity, see the [activity-implementing-rag-with-faiss-and-sentence-embedding.md](activity-implementing-rag-with-faiss-and-sentence-embedding.md) file.
