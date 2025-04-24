# Multi-Source RAG Assistant with Dual Vector Stores and LangChain Integration



## Overview

In this hands-on activity, you'll build an enhanced RAG (Retrieval-Augmented Generation) system that processes multiple document types and implements advanced features needed in production environments. You'll create a system that ingests PDF documents, web pages (including WikiBooks), and CSV data, stores them in two different vector databases for comparison, and provides responses with proper source attribution and streaming output. This implementation focuses on document processing, vector embeddings, and retrieval mechanisms using the LangChain framework.

This project is built on the LangChain framework, which provides a comprehensive ecosystem for building RAG applications. LangChain is used throughout the system for document loading, text splitting, embeddings, vector storage, and retrieval, creating a complete end-to-end RAG pipeline.



## Learning Objectives

By completing this activity, you will be able to:
1. Implement a complete RAG workflow that integrates multiple document sources and document types.
2. Use vector embeddings for semantic search and retrieval.
3. Compare the performance and characteristics of different vector store implementations.
4. Implement source attribution to ensure transparency in generated responses.
5. Build a modular RAG system with components that can be independently adjusted and optimized.



## Time Estimate

120 minutes



## Prerequisites

- Python 3.8+
- Basic understanding of RAG systems and vector embeddings
- Familiarity with Python libraries and package installation



## Setup Instructions

### Step 1: Clone the Repository

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
langchain
langchain-community
faiss-cpu
chromadb
bs4
pypdf
pandas
requests
sentence-transformers
```



## Activity Tasks

The following tasks are organized to guide you through implementing a complete RAG pipeline using the LangChain framework with dual vector stores.

### Task 1: Explore the Sample Documents and Data Sources (10 minutes)

Start by exploring the diverse document sources that will power your RAG system.

1. Examine the files in the `data/books` directory.

2. Open and review a few pages of each PDF to understand their content:
   - `BAGuidebook2.pdf`: A business analysis guidebook with methodologies and best practices
   - `Find_Employment.pdf`: A guide to job-seeking strategies and career development
   - `Managing_Groups_and_Teams.pdf`: Information about team management and group dynamics

3. Open `data/metadata.csv` to understand the additional sources that will be loaded:
   - Note that three WikiBooks will be automatically scraped from the Wikibooks website:
     - Crowdsourcing (https://en.wikibooks.org/wiki/Crowdsourcing)
     - Communication Theory (https://en.wikibooks.org/wiki/Communication_Theory)
     - E-Commerce and E-Business (https://en.wikibooks.org/wiki/E-Commerce_and_E-Business)
   - These HTML-based books will be scraped, processed into sections, and added to your knowledge base

4. Understand how your completed system will use multiple knowledge sources:
   - PDF files loaded from the local filesystem
   - WikiBooks scraped directly from the web
   - Metadata from the CSV file
   
5. Consider how these different document types will need to be processed and chunked for effective retrieval.



### Task 2: Implement Document Loading and Processing (25 minutes)

In this task, you'll implement the functionality to load and process documents from multiple sources.

1. Open `processors/document_processor.py` in your code editor.

2. Take note of the `load_wikibook` method that's already implemented for you. This specialized scraper uses BeautifulSoup to extract content from WikiBooks and divide it into meaningful sections with proper metadata. You won't need to modify this method, but understanding how it works will help you implement the other document loading functions.

3. Implement the `load_pdf` method to:

   Let's start with PDF loading, which is essential for working with the books in the `data/books` directory. You'll use LangChain's `PyPDFLoader` to extract text from PDF files. First, create a loader instance with the file path. After loading the documents, you'll need to enrich them with metadata that will later help with attribution and source tracking. For each document, add information about where it came from (the file name), what type of document it is ("pdf"), the complete file path for reference, and a unique identifier using `uuid.uuid4()`. This metadata is crucial - without it, users won't know which source provided an answer. Make sure to handle the case where a document might not have any metadata yet by checking if `doc.metadata` exists before adding fields to it. The unique IDs you add will help track document chunks throughout the pipeline and prevent duplication issues.

4. Implement the `load_web_page` method to:

   Next, let's implement the general web page loader. This will be simpler than the WikiBook loader since it doesn't need to understand page structure. Use LangChain's `WebBaseLoader` to fetch and process general web content. Much like with PDFs, you'll need to add appropriate metadata to each document that gets loaded. In this case, add the URL as the source, mark the source type as "web", and assign a unique ID. The web loader might return multiple documents depending on the page structure, so make sure your metadata tagging works in a loop over all returned documents. Later, this metadata will allow your system to properly cite web sources when answering questions.

5. Implement the `load_csv` method to:

   Now let's handle CSV loading, which requires a bit more care because of LangChain version compatibility issues. The CSV loader needs to know which column contains the actual content you want to use (specified by the `content_column` parameter). Implement this with a try-except block that first attempts to use the current LangChain approach of passing the content column directly to the loader. If that raises a TypeError (which happens with some versions), fall back to an alternative approach where you create the loader first and then set the column if the loader has that method. Pay special attention to the metadata handling here - for CSV data, you'll want to track not just the filename but also maintain any row information that might be in the original metadata. This helps users know exactly which row of data contributed to an answer.

6. Finally, implement the `process_documents` method to:

   This method is the cornerstone of your document processing pipeline. It takes whole documents and transforms them into right-sized chunks that are optimal for embedding and retrieval. First, create an empty list to store the processed chunks. For each document, grab its metadata and then make a crucial decision: which text splitter should be used? For WikiBook content (which has a "wikibook" source type), use the specialized markdown splitter; for everything else, use the general recursive character splitter that works well with various content types. After splitting documents into chunks, you need to ensure none of the original metadata is lost - loop through each chunk and copy over all metadata fields from the parent document. Additionally, make sure every chunk has a unique identifier, generating a new one if needed. This careful metadata preservation ensures that even after splitting, you can still trace each text chunk back to its source document, page number, and other important context.

The starter code already provides you with skeleton implementations and TODO comments that outline the steps needed. Pay close attention to how existing metadata is handled in the example code - this pattern of preserving context as documents flow through the pipeline is essential for building a robust RAG system.



### Task 3: Implement Embedding Model Integration (20 minutes)

In this task, you'll implement the embedding functionality that transforms text into vector representations.

1. Open `utils/langchain_integration.py` in your code editor.

2. Implement the `EnhancedHuggingFaceEmbeddings` class to:

   Let's start by enhancing the HuggingFaceEmbeddings class from LangChain to better suit our needs. You'll notice this class extends the base `HuggingFaceEmbeddings` class, allowing us to customize its behavior while keeping all the original functionality. First, set the default model to "sentence-transformers/all-MiniLM-L6-v2" - this model is a great balance of quality and performance for RAG applications. It generates 384-dimensional embeddings that capture semantic meaning well without being too computationally expensive. When implementing the `__init__` method, make sure to properly pass all keyword arguments to the parent class using `super().__init__(**kwargs)`. This ensures that any customization options provided when creating the embeddings instance (like custom model paths or device settings) are properly handled. Don't worry about implementing caching or batch processing here - the parent class already handles those efficiently.

3. Implement the `embed_documents` method to:

   Now implement the method for creating embeddings for multiple documents at once. This method takes a list of text strings and should return a list of vector embeddings (one for each input text). Here's the elegant part: you don't need to reimplement the embedding logic! The parent `HuggingFaceEmbeddings` class already has a robust implementation. Simply call `super().embed_documents(texts)` to leverage the existing functionality. This approach follows the principle of code reuse and ensures that any future improvements to the underlying embedding method will automatically benefit your implementation. The method signature shows that it returns `List[List[float]]` - this is because each document is represented by a list of floating-point values (typically 384 values for the model we're using), and you're returning one such list for each document.

4. Implement the `embed_query` method to:

   Finally, implement the query embedding method. This works just like the document embedding method but is optimized for single text inputs (like user questions). Again, the parent class already has a robust implementation, so you just need to call `super().embed_query(text)`. It's crucial that queries are embedded using exactly the same model and process as documents - this ensures that the vector similarity search will work correctly. The slight difference in the return type (`List[float]` rather than `List[List[float]]`) reflects that you're embedding just one piece of text rather than a list of documents. Embedding consistency between documents and queries is essential for your RAG system's accuracy.

The embedding model serves as the foundation for how your system understands both documents and user queries. By implementing these methods properly, you ensure that the semantic meaning of text is captured consistently throughout the system.



### Task 4: Implement Dual Vector Store Setup (25 minutes)

In this task, you'll implement the vector store functionality that powers your retrieval system.

1. Open `vector_stores/vector_store_manager.py` in your code editor.

2. Implement the `initialize_stores` method to:

   This method sets up both vector stores with an initial set of documents. Start by validating that the documents list isn't empty - trying to initialize vector stores with no documents would cause errors downstream. If the list is empty, raise a descriptive ValueError to fail fast and clearly. 
   
   **Important Note:** Unlike in previous modules where FAISS was saved to a .pkl file for persistence, in this implementation FAISS will be used as an in-memory vector store only. This architectural decision allows us to contrast the performance characteristics of an in-memory store (FAISS) with a persistent store (Chroma).
   
   For the FAISS vector store, use `FAISS.from_documents()` to create an in-memory index with the provided documents and embedding model. FAISS is particularly efficient for in-memory similarity search, which makes it perfect for quick lookups. Note that we won't be saving this index to disk with `FAISS.save_local()` as you might have seen in other implementations.
   
   For the Chroma vector store, use `Chroma.from_documents()` with the same documents and embedding model, but also provide the persistence directory where Chroma will store its data. After creating the Chroma store, don't forget to call the `persist()` method to ensure data is written to disk - this is a common oversight that can lead to data loss. Finally, print a confirmation message showing how many documents were indexed. This approach of maintaining dual vector stores lets you compare their performance and leverage their respective strengths.

3. Implement the `add_documents` method to:

   This method adds new documents to existing vector stores or creates new ones if needed. Start with a simple check - if the document list is empty, just return immediately to avoid unnecessary processing. For the FAISS store, check if it already exists. If it does, use `add_documents()` to efficiently add new content; if not, create a new store with `FAISS.from_documents()`. Again, note that we're keeping FAISS entirely in-memory and not persisting it to disk.
   
   Follow the same pattern for the Chroma store, but remember the crucial step of calling `persist()` after adding documents to ensure changes are written to disk. Having two separate code paths (adding to existing vs. creating new) makes your implementation flexible enough to handle both initial setup and ongoing updates to the knowledge base. This is important for real-world RAG systems that may need to incorporate new documents over time.

4. Implement the `query_stores` method to:

   Here's where you'll create the logic to query both vector stores and compare their results. Start by creating an empty dictionary to store the results from both stores. When querying the FAISS store, wrap the call to `similarity_search()` with time measurements using `time.time()` before and after. Store both the retrieved documents and the retrieval time in the results dictionary. This will be valuable for performance analysis. Do the same for the Chroma store, creating a parallel structure in the results dictionary. The `top_k` parameter controls how many documents to retrieve - typically a value around 4 works well for RAG applications. Measuring and storing the retrieval times alongside the documents allows your system to provide insights into the performance characteristics of different vector store implementations, which can help users make informed decisions about which one to use for different scenarios.

5. Implement the `get_retriever` method to:

   This method creates a standardized retriever interface for a specified vector store. First, check which store the user requested (converting to lowercase for case-insensitive matching). If they asked for "faiss", verify that the FAISS store exists before returning its retriever with appropriate search parameters (setting `k=4` for the number of documents to retrieve). If they requested "chroma", do the same check and retriever creation for the Chroma store. If the requested store doesn't exist or isn't recognized, raise a ValueError with a clear message explaining what went wrong. This method creates a consistent interface that higher-level code can use without worrying about the details of each vector store implementation. The consistent `k=4` parameter ensures that retrieval behavior is comparable across different stores.

The vector store manager is the heart of your system's retrieval capabilities. By implementing both FAISS and Chroma stores, you get to experience the trade-offs between different approaches:

- **FAISS**: Implemented as an in-memory only store in this application. This means it's typically faster for retrieval operations but will need to be rebuilt each time the application restarts. No .pkl file is created or used for persistence.

- **Chroma**: Implemented as a persistent store that saves its data to disk in the chroma_db directory. This allows it to maintain its state between application restarts but may have different performance characteristics compared to the in-memory FAISS store.

This dual approach allows you to compare both implementations and understand the trade-offs between speed and persistence in vector store design.



### Task 5: Create the RAG Application Interface (20 minutes)

In this task, you'll implement the main application functionality that connects all components into a cohesive RAG system.

1. Open `app.py` in your code editor.

2. Implement the `add_documents` method to:

   This method serves as the central document ingestion pipeline for your RAG system. First, you'll need to process the raw documents into appropriate chunks using the document processor you implemented earlier. Call `self.doc_processor.process_documents(documents)` to split documents into chunks while preserving metadata. Next, add these processed documents to the internal tracking list with `self.documents.extend(processed_docs)`. This tracking is crucial for features like reloading vector stores. Then, check if this is the first time adding documents by seeing if the FAISS store exists in the vector store manager. If it doesn't exist yet, initialize both vector stores with `self.vector_store_manager.initialize_stores(processed_docs)`. If stores already exist, simply add the new documents to them with `self.vector_store_manager.add_documents(processed_docs)`. This approach handles both initial loading and incremental updates elegantly. The method doesn't return anything since its purpose is to modify the internal state of the RAG system.

3. Implement the `query` method to:

   This is the central method that users will interact with most often. Start by checking if the question is a special command (starting with "/") and route it to the `_handle_command` method if so. Also check if the user requested a comparison between vector stores (when `vector_store` is "both") and use the `compare_vector_stores` method in that case. For normal queries, get the appropriate retriever from the vector store manager based on the requested store name. Next, create a prompt template that instructs the LLM to answer based only on the provided context. This is crucial for grounding the model's responses in the retrieved documents. Create a `PromptTemplate` with this template text and variables for "context" and "question". Then, set up a `RetrievalQA` chain that connects the LLM, retriever, and prompt. Make sure to set `return_source_documents=True` so you can provide attribution. When executing the chain, pass the user's question as the "query" parameter. Finally, handle the response differently based on whether streaming is enabled - if streaming, print the sources separately after the response; if not, format a complete response with sources included. This method essentially orchestrates the entire RAG process from query to response.

4. Implement the `_format_source_info` method to:

   This helper method creates a readable representation of source documents for attribution. Start by checking if there are any source documents at all - if not, return a simple "No sources found" message. Create an empty list to store the formatted source information and a set to track sources you've already seen (to avoid duplicates). For each document, extract its metadata and create a unique identifier combining the source and source type. If you've already seen this source, skip it to avoid duplication. Otherwise, format the source information differently based on the document type: for PDFs, include the page number; for web pages, just show the URL; for WikiBooks, include the title and section; for CSV files, include the row if available. Add each formatted source to your list with a numbering system like "[1]", "[2]", etc. Finally, join all the formatted sources with newlines and return the resulting string. This careful formatting ensures that users can easily trace information back to its original source, which is essential for building trust in AI-generated responses.

These implementations will come together to create a complete RAG system that can load multiple document types, embed them efficiently, retrieve relevant content from dual vector stores, and generate responses with proper source attribution.



### Task 6: Test and Optimize Your Implementation (20 minutes)

Test your complete RAG pipeline and evaluate its performance across all document types.

1. Run your implementation with `python app.py`.

2. Try different types of queries to test your system:
   - Factual questions about specific topics in your PDFs
   - Questions about communication theory, crowdsourcing, or e-commerce to test WikiBook retrieval
   - Comparative questions that require information from multiple sources

3. Verify that all document types are being properly searched:
   - Use specific questions that should retrieve content from WikiBooks
   - Check that PDF documents are properly cited with page numbers
   - Ensure the metadata from CSV is properly integrated

4. Compare the results from different vector stores:
   - Use the `/compare` command to directly compare FAISS and Chroma
   - Note differences in retrieval time, document diversity, and response quality

5. Test the special commands:
   - Use `/reload faiss` to reset and rebuild the FAISS store
   - Use `/reload chroma` to reset and rebuild the Chroma database

This comprehensive testing ensures your RAG system effectively utilizes all knowledge sources, including the WikiBooks scraped from the web, PDFs from the file system, and metadata from CSV.



## Project Structure

```
starter_code/                # Starter code directory
├── app.py                   # Main application file
├── utils/                   # Utility modules
│   └── langchain_integration.py  # LangChain integration
├── processors/              # Document processing modules
│   └── document_processor.py
├── vector_stores/           # Vector store implementations
│   └── vector_store_manager.py
├── data/                    # Data directory
│   ├── metadata.csv         # Book metadata
│   └── books/               # PDF books
│       ├── BAGuidebook2.pdf
│       ├── Find_Employment.pdf
│       └── Managing_Groups_and_Teams.pdf
├── chroma_db/               # Chroma vector database (persistent)
└── requirements.txt         # Project dependencies
```

Note that unlike some other FAISS implementations, this project does not include a FAISS .pkl file for persistence. The FAISS vector store is maintained entirely in memory and rebuilt when needed, while Chroma provides the persistent storage option.



## Starter Code and Solution Code

Both the `starter_code` and `solution` directories contain implementations of the RAG system with LangChain and dual vector stores. The `starter_code` directory is intended for students to use as a starting point, while the `solution` directory provides a reference implementation.



## Interactive Commands Reference

The application includes a comprehensive interactive command-line interface that allows you to interact with your RAG system. Here's a detailed reference of all available commands:

### Natural Language Queries

**Description:** Enter any natural language question to query the system.

**Example:** `What is crowdsourcing?`

**Behavior:** The system will retrieve relevant documents from the default vector store (FAISS), generate a response based on the retrieved context, and display the response with source attribution.

### `/compare <query>`

**Description:** Compare results from both FAISS and Chroma vector stores for the same query.

**Example:** `/compare What are the key aspects of e-commerce?`

**Behavior:** The system will:
1. Retrieve documents from both FAISS and Chroma
2. Display retrieval time for each store
3. Show the number of documents retrieved from each store
4. Generate and display responses from both sets of retrieved documents
5. Compare performance metrics between the two stores

This command is particularly useful for understanding the different retrieval patterns between FAISS and Chroma.

### `/faiss <query>`

**Description:** Query using only the FAISS vector store.

**Example:** `/faiss What is communication theory?`

**Behavior:** The system will retrieve documents from FAISS, generate a response, and display it with source attribution. This is useful when you specifically want to leverage FAISS's higher recall and diversity of results.

### `/chroma <query>`

**Description:** Query using only the Chroma vector store.

**Example:** `/chroma How do teams handle conflicts?`

**Behavior:** The system will retrieve documents from Chroma, generate a response, and display it with source attribution. This is useful when you want to leverage Chroma's higher precision and focus on highly similar documents.

### `/reload faiss`

**Description:** Clear and rebuild the FAISS vector store with existing documents.

**Example:** `/reload faiss`

**Behavior:** The system will:
1. Reset the FAISS store
2. Re-index all previously added documents
3. Display timing information and document count
4. Confirm when the reload is complete

This command is useful after adding new documents or when you want to ensure consistent vector representations.

### `/reload chroma`

**Description:** Delete and rebuild the Chroma database with existing documents.

**Example:** `/reload chroma`

**Behavior:** The system will:
1. Delete the existing Chroma database directory
2. Create a new Chroma database
3. Re-index all previously added documents
4. Display timing information, document count, and persistence directory
5. Confirm when the reload is complete

This command is useful when you want to reset the persistent Chroma database or after adding new documents.

### `/reload vectordb`

**Description:** Reload both FAISS and Chroma vector stores.

**Example:** `/reload vectordb`

**Behavior:** The system will execute both `/reload faiss` and `/reload chroma` sequentially, rebuilding both vector stores with existing documents.

### `/run demo`

**Description:** Run a predefined demonstration of the system's capabilities.

**Example:** `/run demo`

**Behavior:** The system will:
1. Create a new RAG instance
2. Add sample documents (WikiBooks, PDFs, CSV)
3. Run example queries with both FAISS and Chroma
4. Compare vector stores with a sample query
5. Return to interactive mode when complete

This command is useful for quickly seeing the system's capabilities without manually entering multiple commands.

### `/help`

**Description:** Display the help menu with available commands.

**Example:** `/help`

**Behavior:** The system will display a list of all available commands with brief descriptions.

### `/exit`

**Description:** Exit the interactive mode and terminate the application.

**Example:** `/exit`

**Behavior:** The system will display a session summary (number of queries processed) and exit.



## Extension Options

1. **Add Query Caching**: Implement a caching mechanism that stores previous query results to improve response time for repeated or similar queries.

2. **Implement Cross-Store Retrieval Fusion**: Create an advanced retrieval mechanism that combines results from both vector stores, using techniques like reciprocal rank fusion to produce better overall results.

3. **Add Document Refreshing**: Implement a mechanism to update documents in the knowledge base when their source content changes, handling the synchronization between the original source and the vector stores.

4. **Implement Hybrid Search**: Combine vector search with keyword search for better retrieval performance, especially for factual queries.
