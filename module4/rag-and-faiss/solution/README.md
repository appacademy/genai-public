# RAG Implementation with FAISS and Sentence Embeddings

This project implements a Retrieval-Augmented Generation (RAG) system using FAISS as a vector database and sentence embeddings. It's designed as a learning activity for students studying Generative AI for Software Developers.

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
python app-FINAL.py
```

Or, if you're working through the activity:

```bash
python app-STARTER.py
```

## Special Commands

When running the application, you can use these special commands:

- `reload`: Delete and recreate the FAISS index (useful when you make changes to your implementation)
- `exit`: Exit the program

## Activity Instructions

For detailed instructions on completing the activity, see the [activity-implementing-rag-with-faiss-and-sentence-embedding.md](activity-implementing-rag-with-faiss-and-sentence-embedding.md) file.
