# LangChain RAG System: Integrating Ollama for Local LLM Inference



## Overview

This activity is Part 2 of the LangChain RAG module. Building upon the multi-source RAG pipeline with dual vector stores you implemented in Part 1, this activity focuses on integrating a local Large Language Model (LLM) using Ollama and the Gemma 3 4B model. You will connect the retrieval components (document processing, embeddings, vector stores) with the generation component (Ollama LLM) to create a complete, end-to-end RAG system capable of answering questions based on the retrieved context from your documents.

This project utilizes the LangChain framework to orchestrate the integration, specifically using the `RetrievalQA` chain to combine the retriever and the LLM.



## Learning Objectives

By completing this activity, you will be able to:

1.  Understand the role of the LLM in a RAG system.
2.  Integrate a LangChain-compatible Ollama wrapper (`OllamaLLM`) into an existing RAG pipeline.
3.  Configure and initialize the `OllamaLLM` component with appropriate parameters (model name, temperature, API URL).
4.  Connect the LLM with a vector store retriever using LangChain's `RetrievalQA` chain.
5.  Generate responses grounded in retrieved document context using the integrated local LLM.
6.  Observe how streaming responses are handled when using the Ollama integration.



## Time Estimate

60 minutes



## Prerequisites

-   Python 3.12 (as used in the project setup)
-   Ollama installed and running locally
-   Gemma 3 4B model pulled in Ollama (`ollama pull gemma3:4b`)
-   Completion of Part 1: Multi-Source RAG Assistant with Dual Vector Stores activity.
-   Basic understanding of LangChain components (LLMs, Chains, Retrievers, Prompts).
-   Familiarity with the codebase from Part 1 (`document_processor.py`, `vector_store_manager.py`, `embeddings_fixed.py`).



## Setup Instructions



1. ### Step 1: Clone the Repository

   Clone the starter code repository to your local machine:

   ```bash
   git clone https://github.com/[organization]/langchain-rag-pipeline.git
   cd langchain-rag-pipeline
   ```

   

   ### Step 2: Create and Activate a Virtual Environment

   Create and then activate a virtual environment for your project using the commands for your system:

   - **Mac/Linux**:

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

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

   After activation, your terminal prompt should change (e.g., `(venv)` appears).

   

   ### Step 3: Install Dependencies

   With the virtual environment active, install the required packages:

   ```bash
   cd starter_code
   pip install -r requirements.txt
   ```

   The requirements.txt file contains the following dependencies:

   ```
   # Core dependencies
   langchain-core==0.1.33
   langchain-text-splitters==0.0.1
   langchain-community>=0.0.28,<0.1
   langchain==0.1.12
   python-dotenv==1.0.1
   
   # Vector storage and embedding
   sentence-transformers==2.6.0
   # Using a pre-built wheel for faiss-cpu and specific torch version
   torch==2.3.0+cpu # Updated torch version based on availability
   --find-links https://download.pytorch.org/whl/torch_stable.html
   faiss-cpu
   chromadb==0.4.22
   transformers==4.36.2 # Added compatible transformers version
   accelerate==0.25.0 # Added compatible accelerate version
   
   # Document processing
   pypdf==4.1.0
   beautifulsoup4==4.12.3
   
   # Network and API
   requests==2.31.0
   ```



### Step 4: Ensure Ollama is Running

Ensure Ollama is running in a separate terminal with the Gemma 3 4B model active:

```bash
ollama run gemma3:4b
```

Keep this terminal running throughout the activity.



## Activity Tasks

The following tasks guide you through integrating the Ollama LLM into the RAG pipeline you built in Part 1.

### Task 1: Understand the Ollama LLM Wrapper (10 minutes)

Before integrating, familiarize yourself with the provided Ollama LLM wrapper.

1.  Open `models/ollama_integration_fixed.py`.
2.  Review the `OllamaLLM` class structure:
    *   It inherits from LangChain's `LLM` base class.
    *   It uses standard Pydantic fields for configuration (`model_name`, `temperature`, `api_url`, etc.).
    *   The `__init__` method initializes the parent class and performs an API health check.
    *   The `_call` method handles standard (non-streaming) requests to the Ollama `/api/generate` endpoint using the `requests` library.
    *   The `_stream` method handles streaming requests to the same endpoint, yielding `GenerationChunk` objects.
3.  Note the key parameters: `model_name`, `temperature`, `api_url`, `timeout`, `debug_prompts`, `debug_stream`.



### Task 2: Integrate the Ollama LLM into EnhancedRAG (25 minutes)

In this task, you will integrate the Ollama Large Language Model (LLM) into the main RAG application class, connecting the retrieval pipeline built in Part 1 with the generation capabilities of the local LLM.

1.  Open `rag/enhanced_rag.py` in your code editor. This file contains the `EnhancedRAG` class which orchestrates the entire process.

2.  First, ensure the `OllamaLLM` class is available within this file.

    **Step 2.1**. Find the TODO comment: "Task 2a - Integrate the Ollama LLM into EnhancedRAG class" and follow the steps below.
    
    **Step 2.2**. Find the TODO comment: "Import OllamaLLM from models.ollama_integration_fixed" and add this code snippet:
    
    ```python
    from models.ollama_integration_fixed import OllamaLLM
    ```
    
    This code imports the `OllamaLLM` class from the `models.ollama_integration_fixed` module, which will allow you to use Ollama's language models in your application.


3.  Next, locate the `__init__` method of the `EnhancedRAG` class.

    The `__init__` method in Python is the constructor, responsible for initializing new objects of the class. Similar to constructors in Java or C#, it sets up the initial state of the instance. Here, you need to initialize the LLM component.

    **Step 3.1**. Find the TODO comment: "Task 2b - Initialize the OllamaLLM component" and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "Instantiate OllamaLLM, passing the relevant parameters" and add this code snippet:
    
    ```python
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
    ```
    
    This code initializes the streaming settings and creates an instance of the OllamaLLM class with the configuration parameters passed to the EnhancedRAG constructor. It sets the model name, temperature for text generation, API URL, debugging options, and a timeout value. The OllamaLLM instance is assigned to `self.llm` so it can be used throughout the EnhancedRAG class.
    
    **Step 3.3**. Find the TODO comment: "Initialize the remaining components" and add this code snippet:
    
    ```python
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
    ```
    
    This code initializes the embedding model using SentenceTransformerEmbeddings, sets up the document processor with the specified chunk size and overlap, configures the vector store manager with the embedding model and persistence directory, and creates an empty list to track documents.
    
    **Step 3.4**. Find the TODO comment: "Print initialization information" and add this code snippet:
    
    ```python
    print("\n" + "=" * 60)
    print("ENHANCED RAG SYSTEM INITIALIZED")
    print("=" * 60)
    print("* Document types: PDF, WikiBook, Web pages, CSV")
    print("* Embeddings: SentenceTransformer (all-MiniLM-L6-v2)")
    print("* Vector stores: FAISS (in-memory), Chroma (persistent)")
    print(f"* LLM: Ollama ({model})")
    print("* Special commands: /reload faiss, /reload chroma, /reload vectordb")
    print("=" * 60 + "\n")
    ```
    
    This code prints formatted information about the initialized RAG system, including supported document types, embedding model, vector stores, LLM configuration, and special commands available to the user.


4.  Now, locate the `query` method within the `EnhancedRAG` class.    

    This method handles user queries, retrieves relevant documents, and generates a response. The core of the RAG process here involves using LangChain's `RetrievalQA` chain, which links the retriever (providing context) to the LLM (generating the answer). Your task is to ensure that the `llm` parameter within this call is correctly assigned the `self.llm` instance you initialized in the `__init__` method. This step connects the specific Ollama LLM instance you configured to the LangChain chain responsible for generation.

    Take a moment to review the logic inside the `if use_streaming:` block. Notice how it directly calls `self.llm.stream(...)` under certain conditions. This demonstrates an alternative way to interact with the LLM wrapper for streaming, separate from the main `RetrievalQA` chain execution, showcasing the flexibility of the LangChain components. 

    **Step 4.1**. Find the TODO comment: "Task 4 - Implement the query method" and follow the steps below.
    
    **Step 4.2**. Find the TODO comment: "Handle streaming settings and special commands" and add this code snippet:
    
    ```python
    # Use instance streaming setting if not specified
    use_streaming = (
        self.streaming if streaming is None else streaming
    )

    # Check for special commands
    if question.startswith("/"):
        return self._handle_command(question)

    if vector_store.lower() == "both":
        return self.compare_vector_stores(question)
    ```
    
    This code determines whether to use streaming based on the instance default or the parameter value. It also checks for special commands that start with "/" and handles the case where the user wants to compare results from both vector stores.
    
    **Step 4.3**. Find the TODO comment: "Get retriever and create prompt template" and add this code snippet:
    
    ```python
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
    ```
    
    This code gets the appropriate retriever based on the specified vector store and creates a prompt template that instructs the LLM how to answer questions based on the provided context.
    
    **Step 4.4**. Find the TODO comment: "Create the LangChain RetrievalQA chain" and add this code snippet:
    
    ```python
    # Create a RetrievalQA chain - use the existing LLM instance
    qa_chain = RetrievalQA.from_chain_type(
        llm=self.llm,  # Use the existing LLM instance
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
        callbacks=self.callbacks if use_streaming else None, 
    )
    ```
    
    This code creates a RetrievalQA chain using the LangChain framework. It connects your LLM instance with the retriever to form a complete RAG pipeline.
    
    **Step 4.5**. Find the TODO comment: "Implement streaming response handling" and add this code snippet:
    
    ```python
    if use_streaming:
        # --- Manual Streaming Logic ---
        print("Attempting manual streaming...")
        # 1. Retrieve documents
        retrieved_docs = retriever.get_relevant_documents(question)
        print(
            f"Retrieved {len(retrieved_docs)} documents for manual streaming."
        )

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
        print("\n--- End Streaming Response ---")  # Add a newline after streaming

        # 5. Format and print sources
        formatted_sources = self._format_source_info(retrieved_docs)
        print("\n\nSources:\n")
        print(formatted_sources)
        return f"\nSources:\n{formatted_sources}"  # Return sources like before
    ```
    
    This code implements manual streaming by retrieving documents, formatting the context and prompt, and then streaming the response directly from the LLM. It also formats and returns the source information.
    
    **Step 4.6**. Find the TODO comment: "Implement non-streaming response handling" and add this code snippet:
    
    ```python
    else:
        # --- Original Non-Streaming Logic ---
        # Execute the chain
        chain_response = qa_chain({"query": question})

        # Format response with sources for non-streaming case
        full_response = self._format_response_with_sources(
            chain_response.get("result", "No response generated."),
            chain_response["source_documents"],
        )
        return full_response
    ```
    
    This code handles the non-streaming case by executing the QA chain with the user's question and then formatting the response with source attribution.


### Task 3: Test the Integrated RAG System (25 minutes)

With the LLM integrated, test the complete end-to-end RAG workflow.

1.  Run the application from your terminal:
    ```bash
    python app.py
    ```
    Ensure Ollama is running `gemma3:4b` in another terminal.
2.  Wait for the application to initialize and load the documents into the vector stores.
3.  Enter natural language queries related to the documents loaded in Part 1 (e.g., PDFs, WikiBooks):
    *   `What are the key strategies for finding employment?`
    *   `What is crowdsourcing?`
    *   `Summarize the main points about managing teams.`
    *   `What is e-commerce?` (Test WikiBook retrieval)
4.  Observe the output:
    *   You should see the LLM generating responses based on the context retrieved from the FAISS vector store (the default).
    *   The responses should be streamed to the console.
    *   Source attribution should appear after the response, indicating which documents were used.
5.  Test the available commands:
    *   `/reload vectordb`: Verify that it re-indexes documents into both stores.
    *   `/help`: Check the displayed commands.
    *   `/exit`: Terminate the application.

This testing confirms that the retrieval components (vector stores) and the generation component (Ollama LLM) are working together correctly within the LangChain framework.



## Project Structure

The project structure remains largely the same as in Part 1, but the focus shifts to the interaction between `rag/enhanced_rag.py` and `models/ollama_integration_fixed.py`.

```
/
├── app.py                       # Main application entry point with CLI interface
├── .env                         # Environment variables (Ollama API URL)
├── requirements.txt             # Project dependencies
├── knowledge_transfer.md        # Detailed knowledge transfer document
├── README.md                    # Project README
├── data/                        # Sample documents (PDFs, CSV)
├── chroma_db/                   # Persistent Chroma vector store data
├── models/
│   ├── __init__.py
│   ├── embeddings_fixed.py      # SentenceTransformer embeddings implementation
│   └── ollama_integration_fixed.py # Ollama LLM integration (Focus of this activity)
├── processors/
│   ├── __init__.py
│   └── document_processor.py    # Document loading and processing (From Part 1)
├── managers/
│   ├── __init__.py
│   └── vector_store_manager.py  # Vector store management (From Part 1)
├── rag/
│   ├── __init__.py
│   └── enhanced_rag.py          # Core RAG implementation (Focus of this activity)
└── utils/                       # Utility functions (currently minimal)
    └── __init__.py
```



## Starter Code and Solution Code

-   **Starter Code:** Use the `starter` directory from the main project repository. It should contain the completed code from Part 1, with placeholders (like `TODO` comments) for the LLM integration steps in `rag/enhanced_rag.py`.
-   **Solution Code:** The main project directory represents the completed solution for both Part 1 and Part 2. You can refer to `rag/enhanced_rag.py` in the root directory to see the final implementation.



## Interactive Commands Reference

The interactive mode provides a simplified interface focused on querying the integrated RAG system:

```
• Any natural language query (e.g., "What are the best practices for team management?")
• /reload vectordb - Rebuild both FAISS and Chroma vector stores from loaded documents
• /help            - Show this help menu
• /exit            - Exit interactive mode
```

Note that commands related to comparing or selecting specific vector stores (`/compare`, `/faiss`, `/chroma`) are not present in this version, as the system defaults to using FAISS via the `EnhancedRAG.query` method.



## Conclusion

In this activity, you successfully integrated a local LLM (Gemma 3 4B via Ollama) into your LangChain RAG pipeline. You connected the retrieval components built in Part 1 with the `OllamaLLM` wrapper, enabling the system to generate context-aware answers based on your specific documents. This completes the core RAG workflow, demonstrating how to leverage local models for enhanced privacy, cost-effectiveness, and customization in AI applications.
