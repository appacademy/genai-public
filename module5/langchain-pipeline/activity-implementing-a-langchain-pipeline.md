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

- Python 3.12
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
  python3 -m venv venv
  source .venv/bin/activate
  ```

- **Windows (PowerShell)**:

  ```bash
  python -m venv venv
  .\.venv\Scripts\activate
  ```

- **Windows (Command Prompt)**:

  ```bash
  python -m venv .venv
  venv/Scripts/activate
  ```

After activation, your terminal prompt should change (e.g., `(venv)` appears).

### Step 3: Install Dependencies

With the virtual environment active, install the required packages:

```bash
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

    **Step 1.1**. Find the TODO comment: "Task 2a - Implement Webscraping, Loading, and Processing" and follow the steps below.

	**Step 1.2**. Find the TODO comment: "Implement specialized WikiBook scraping using BeautifulSoup" and add this code snippet:
    
    ```python
    try:
        # Fetch the content
        response = requests.get(url)
        response.raise_for_status()
    
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
    ```
    
    This code fetches the content from the provided URL and parses it using BeautifulSoup, which is a Python library for extracting data from HTML and XML files.

    **Step 1.3**. Find the TODO comment: "Extract the title and main content from the WikiBook" and add this code snippet:
    
    ```python
    # Extract the title
    title = soup.find("h1", {"id": "firstHeading"}).text.strip()
    
    # Extract the main content
    content_div = soup.find("div", {"id": "mw-content-text"})
    
    # Remove unwanted elements
    for unwanted in content_div.select(
        ".navbox, .vertical-navbox, .ambox, .mbox-small, .noprint, .mw-empty-elt"
    ):
        unwanted.decompose()
    ```
    
    This code extracts the title of the WikiBook from the h1 element with id "firstHeading", finds the main content div, and removes unwanted elements like navigation boxes and other non-content elements.

    **Step 1.4**. Find the TODO comment: "Process the content by sections with headings" and add this code snippet:
    
    ```python
    # Extract all sections with their headings
    sections = []
    current_heading = None
    current_content = []
    
    for element in content_div.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "table"]
    ):
        if element.name.startswith("h"):
            # Save the previous section
            if current_heading and current_content:
                section_text = f"# {current_heading}\n\n" + "\n".join(
                    current_content
                )
                sections.append(section_text)
    
            # Start a new section
            current_heading = element.text.strip()
            current_content = []
        else:
            # Add content to the current section
            if element.name == "p":
                current_content.append(element.text.strip())
            elif element.name in ["ul", "ol"]:
                for li in element.find_all("li"):
                    current_content.append(f"- {li.text.strip()}")
            elif element.name == "table":
                # Simplified table extraction
                table_text = "Table: "
                for row in element.find_all("tr"):
                    cells = [
                        cell.text.strip() for cell in row.find_all(["th", "td"])
                    ]
                    if cells:
                        table_text += " | ".join(cells) + "\n"
                current_content.append(table_text)
    
    # Add the last section
    if current_heading and current_content:
        section_text = f"# {current_heading}\n\n" + "\n".join(current_content)
        sections.append(section_text)
    ```
    
    This code processes the content by finding all headings and content elements. It organizes the content into sections based on headings, and formats different types of content (paragraphs, lists, tables) appropriately.

    **Step 1.5**. Find the TODO comment: "Create Document objects with appropriate metadata" and add this code snippet:
    
    ```python
    # Create documents from sections
    documents = []
    for i, section in enumerate(sections):
        doc = Document(
            page_content=section,
            metadata={
                "source": url,
                "source_type": "wikibook",
                "title": title,
                "section": i,
                "doc_id": str(uuid.uuid4()),
            },
        )
        documents.append(doc)
    
    return documents
    ```
    
    This code creates Document objects for each section, with metadata including the source URL, source type, title, section number, and a unique document ID.

    **Step 1.6**. Find the TODO comment: "Include error handling with fallback to standard web page loading" and add this code snippet:
    
    ```python
    except Exception as e:
        print(f"Error loading WikiBook from {url}: {str(e)}")
        # Fallback to standard WebBaseLoader
        print("Falling back to standard WebBaseLoader")
        return self.load_web_page(url)
    ```
    
    This code provides error handling in case the WikiBook scraping fails. It prints an error message and falls back to using the standard web page loader method.



2. Implement the `load_pdf` method. PDF loading is essential for working with the books in the `data/books` directory. You'll use LangChain's `PyPDFLoader` to extract text from PDF files. Each document object will contain information about where it came from (the file name), what type of document it is ("pdf"), the complete file path for reference, and a unique identifier using `uuid.uuid4()`.    

    **Step 2.1**. Find the TODO comment: "Task 2b - Implement PDF Loading and Processing" and follow the steps below.
    
    **Step 2.2**. Find the TODO comment: "Use PyPDFLoader to load the PDF file" and add this code snippet:
    
    ```python
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    ```
    
    This code creates a PyPDFLoader instance with the provided file path and uses it to extract text from the PDF file, returning a list of Document objects.
    
    **Step 2.3**. Find the TODO comment: "Add appropriate metadata to each document (source, source_type, file_path)" and add this code snippet:
    
    ```python
    # Add source metadata
    file_name = os.path.basename(file_path)
    for doc in documents:
        if not doc.metadata:
            doc.metadata = {}
        doc.metadata["source"] = file_name
        doc.metadata["source_type"] = "pdf"
        doc.metadata["file_path"] = file_path
    ```
    
    This code extracts the file name from the path and adds important metadata to each document, including the source (file name), source type ("pdf"), and the complete file path for reference.
    
    **Step 2.4**. Find the TODO comment: "Add a unique ID for each document" and add this code snippet:
    
    ```python
    # Add unique ID for each document chunk
    doc.metadata["doc_id"] = str(uuid.uuid4())
    ```
    
    This code adds a unique identifier to each document using `uuid.uuid4()`, which helps track document chunks throughout the pipeline and prevents duplication issues.
    
    **Step 2.5**. Return the processed documents:
    
    ```python
    return documents
    ```
    
    This code returns the list of Document objects with all the added metadata.


3. Next, let's implement the general web page loader using the `load_web_page` method. This will be simpler than the WikiBook loader since it doesn't need to understand page structure. We will add appropriate metadata to each document that gets loaded. The web loader might return multiple documents depending on the page structure, so make sure your metadata tagging works in a loop over all returned documents. Later, this metadata will allow your system to properly cite web sources when answering questions.

    **Step 3.1**. Find the TODO comment: "Task 2c - Implement Web Page Loading and Processing" and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "Use WebBaseLoader to load content from the URL" and add this code snippet:
    
    ```python
    loader = WebBaseLoader(url)
    documents = loader.load()
    ```
    
    This code uses LangChain's WebBaseLoader to fetch and process the content from the provided URL.
    
    **Step 3.3**. Find the TODO comment: "Add appropriate metadata to each document (source, source_type)" and add this code snippet:
    
    ```python
    # Add source metadata
    for doc in documents:
        if not doc.metadata:
            doc.metadata = {}
        doc.metadata["source"] = url
        doc.metadata["source_type"] = "web"
    ```
    
    This code adds metadata to each document, including the URL as the source and marking the source type as "web". The web loader might return multiple documents depending on the page structure, so this loop ensures all documents get the proper metadata.
    
    **Step 3.4**. Find the TODO comment: "Add a unique ID for each document" and add this code snippet:
    
    ```python
    # Add unique ID for each document chunk
    doc.metadata["doc_id"] = str(uuid.uuid4())
    ```
    
    This code assigns a unique identifier to each document using UUID. This will help with tracking and referencing documents later when the system needs to cite web sources.
    
    **Step 3.5**. Return the processed documents:
    
    ```python
    return documents
    ```
    
    This code returns the list of documents with all the necessary metadata added.


4. Now let's handle CSV loading by implementing the `load_csv` method. This requires a bit more care because of LangChain version compatibility issues. The CSV loader needs to know which column contains the actual content you want to use. Implement this with a try-except block that first attempts to use the current LangChain approach of passing the content column directly to the loader. If that raises a TypeError (which happens with some versions), fall back to an alternative approach where you create the loader first and then set the column if the loader has that method. Pay special attention to the metadata handling here - for CSV data, you'll want to track not just the filename but also maintain any row information that might be in the original metadata. This helps users know exactly which row of data contributed to an answer.

    **Step 4.1**. Find the TODO comment: "Task 2d - Implement CSV Loading and Processing" and follow the steps below.
    
    **Step 4.2**. Find the TODO comment: "Use CSVLoader to load data from the CSV file" and add this code snippet:
    
    ```python
    try:
        # First try with the content_column parameter
        loader = CSVLoader(
            file_path=file_path,
            csv_args={
                "delimiter": ",",
                "quotechar": '"',
            },
            content_column=content_column,
        )
        documents = loader.load()
    except TypeError:
        # If that fails, try the alternative approach
        print(f"Using alternative CSVLoader approach for {file_path}")
        loader = CSVLoader(
            file_path=file_path,
            csv_args={
                "delimiter": ",",
                "quotechar": '"',
            },
        )
    
        # Try to set the column if the method exists
        if hasattr(loader, "set_column"):
            loader.set_column(content_column)
    
        documents = loader.load()
    ```
    
    This code handles LangChain version compatibility issues by first trying to create a CSVLoader with the content_column parameter directly. If that raises a TypeError, it falls back to an alternative approach where it creates the loader first and then sets the column if that method exists.
    
    **Step 4.3**. Find the TODO comment: "Add appropriate metadata to each document" and add this code snippet:
    
    ```python
    # Add source metadata
    file_name = os.path.basename(file_path)
    for doc in documents:
        if not doc.metadata:
            doc.metadata = {}
        doc.metadata["source"] = file_name
        doc.metadata["source_type"] = "csv"
        doc.metadata["file_path"] = file_path
        # Add unique ID for each document chunk
        doc.metadata["doc_id"] = str(uuid.uuid4())
    ```
    
    This code adds important metadata to each document, including the source filename, source type, file path, and a unique ID. This metadata helps track which row of data contributed to an answer.
    
    **Step 4.4**. Find the TODO comment: "Return the processed documents" and add this code snippet:
    
    ```python
    return documents
    ```
    
    This code returns the list of documents with their content and metadata for further processing.


5. Finally, we'll implement the `process_documents` method. This method is the cornerstone of your document processing pipeline. It takes whole documents and transforms them into right-sized chunks that are optimal for embedding and retrieval. The code will determine the appropriate test splitter for each document type. We'll add the metadata to each chunk of text and assign it a unique identifier.

    **Step 5.1**. Find the TODO comment: "Task 2e - Implement Document Chunking" and follow the steps below.
    
    **Step 5.2**. Find the TODO comment: "Create a list to store processed document chunks" and add this code snippet:
    
    ```python
    processed_docs = []
    ```
    
    This code initializes an empty list that will store all the processed document chunks.
    
    **Step 5.3**. Find the TODO comment: "For each document, select the appropriate text splitter based on document type" and add this code snippet:
    
    ```python
    for doc in documents:
        # Store original metadata
        original_metadata = doc.metadata if doc.metadata else {}
    
        # Choose the appropriate splitter based on source type
        splitter = (
            self.markdown_splitter
            if original_metadata.get("source_type") == "wikibook"
            else self.text_splitter
        )
    ```
    
    This code loops through each document, stores its metadata, and selects the appropriate text splitter based on the document type. WikiBook content uses the markdown splitter, while all other content uses the general text splitter.
    
    **Step 5.4**. Find the TODO comment: "Split the document into chunks using the selected splitter" and add this code snippet:
    
    ```python
    # Split the document
    chunks = splitter.split_documents([doc])
    ```
    
    This code uses the selected splitter to break the document into smaller, more manageable chunks for processing.
    
    **Step 5.5**. Find the TODO comment: "Ensure all metadata from the original document is preserved in each chunk" and add this code snippet:
    
    ```python
    # Ensure metadata is preserved in each chunk
    for chunk in chunks:
        if not chunk.metadata:
            chunk.metadata = {}
    
        # Merge original metadata with any new metadata
        for key, value in original_metadata.items():
            if key not in chunk.metadata:
                chunk.metadata[key] = value
    ```
    
    This code ensures that all metadata from the original document is preserved in each chunk by copying over any metadata fields that aren't already present in the chunk.
    
    **Step 5.6**. Find the TODO comment: "Add unique IDs to each chunk if not already present" and add this code snippet:
    
    ```python
    # Ensure each chunk has a unique ID
    if "doc_id" not in chunk.metadata:
        chunk.metadata["doc_id"] = str(uuid.uuid4())
    
    processed_docs.append(chunk)
    ```
    
    This code generates a unique identifier for each chunk if one doesn't already exist, and adds the processed chunk to the list of processed documents.
    
    **Step 5.7**. Find the TODO comment: "Return the processed document chunks" and add this code snippet:
    
    ```python
    return processed_docs
    ```
    
    This code returns the list of processed document chunks for further processing in the pipeline.


### Task 3: Implement Embedding Model Integration (20 minutes)

In this task, you'll implement the embedding functionality that transforms text into vector representations.

1. Let's start by enhancing the HuggingFaceEmbeddings class from LangChain to better suit our needs. You'll notice this class extends the base `HuggingFaceEmbeddings` class, allowing us to customize its behavior while keeping all the original functionality. 
   
   Open `utils/langchain_integration.py` in your code editor.

    **Step 1.1**. Find the TODO comment: "Task 3a - Implement and Initialize the EnhancedHuggingFaceEmbeddings class" and follow the steps below.
   
    **Step 1.2**. Find the TODO comment: "Set the default model to sentence-transformers/all-MiniLM-L6-v2" and add this code snippet:
   
    ```python
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ```
   
    This code sets the default embedding model to "sentence-transformers/all-MiniLM-L6-v2", which provides a good balance between quality and performance for RAG applications. This model generates 384-dimensional embeddings that effectively capture semantic meaning without being too computationally expensive.
   
    **Step 1.3**. Find the TODO comment: "Initialize the parent HuggingFaceEmbeddings class with the provided kwargs" and add this code snippet:
   
    ```python
    def __init__(self, **kwargs):
        """Initialize the EnhancedHuggingFaceEmbeddings."""
        super().__init__(**kwargs)
    ```
   
    This code creates the initialization method that passes all keyword arguments to the parent class using `super().__init__(**kwargs)`. This ensures that any customization options provided when creating the embeddings instance (like custom model paths or device settings) are properly handled by the parent class.


2. Next, we'll implement the method for creating embeddings for multiple documents at once using the `embed_documents` method in your code file. This method takes a list of text strings and returns a list of vector embeddings (one for each input text). Here's the best part: you don't need to reimplement the embedding logic! The parent `HuggingFaceEmbeddings` class already has a robust implementation. The method signature shows that it returns `List[List[float]]` - this is because each document is represented by a list of floating-point values (typically 384 values for the model we're using), and you're returning one such list for each document.

    **Step 2.1**. Find the TODO comment: "Task 3b - Creating embeddings for multiple documents at once" and follow the steps below.
    
    **Step 2.2**. Find the TODO comment: "Use the parent class method to embed multiple documents" and add this code snippet:
    
    ```python
    return super().embed_documents(texts)
    ```
    
    This code calls the parent class's `embed_documents` method to create embeddings for multiple documents at once. It leverages the existing implementation in the `HuggingFaceEmbeddings` class, following the principle of code reuse. The method returns a list of embeddings, where each embedding is a list of floating-point values (typically 384 values for the model we're using).


3. Finally, we'll implement the query embedding in the `embed_query` method. This works just like the document embedding method but is optimized for single text inputs (like user questions). Again, the parent class already has a robust implementation, so you just need to call `super().embed_query(text)`. It's important that queries are embedded using exactly the same model and process as documents - this ensures that the vector similarity search will work correctly. The slight difference in the return type (`List[float]` rather than `List[List[float]]`) reflects that you're embedding just one piece of text rather than a list of documents. Embedding consistency between documents and queries is essential for your RAG system's accuracy.

    **Step 3.1**. Find the TODO comment: "Task 3c - Embed user queries" and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "Use the parent class method to embed a single query text" and add this code snippet:
    
    ```python
    return super().embed_query(text)
    ```
    
    This code calls the parent class's `embed_query` method to embed the query text. This ensures that queries are embedded using the same model and process as documents, which is essential for accurate vector similarity search. The method returns a single list of floats representing the embedding for the query text.

The embedding model serves as the foundation for how your system understands both documents and user queries. When you implement these methods properly, you ensure that the semantic meaning of text is captured consistently throughout the system.

### Task 4: Implement Dual Vector Store Setup (25 minutes)

In this task, you'll implement the vector store functionality that powers your retrieval system.

1. Open `vector_stores/vector_store_manager.py` in your code editor.
   
   This method sets up both vector stores with an initial set of documents. Unlike in a previous module where FAISS was saved to a `.pkl` file for persistence, in this implementation FAISS will be used as an in-memory vector store only. This architectural decision allows us to contrast the performance characteristics of an in-memory store (FAISS) with a persistent store (Chroma).

    **Step 1.1**. Find the TODO comment: "Task 4a - Initialize Dual Vector Stores" and follow the steps below.
   
    **Step 1.2**. Find the TODO comment: "Validate that the documents list is not empty" and add this code snippet:
   
    ```python
    if not documents:
        raise ValueError("Cannot initialize vector stores with empty document list")
    ```
   
    This code checks if the documents list is empty and raises a ValueError with a descriptive message if it is, preventing errors that would occur downstream if we tried to initialize vector stores with no documents.
   
    **Step 1.3**. Find the TODO comment: "Initialize FAISS as an in-memory vector store using the documents and embedding model" and add this code snippet:
   
    ```python
    # Initialize FAISS (in-memory)
    self.faiss_store = FAISS.from_documents(documents, self.embedding_model)
    ```
   
    This code creates an in-memory FAISS vector store using the provided documents and embedding model. FAISS is efficient for in-memory similarity search and will be used for quick lookups.
   
    **Step 1.4**. Find the TODO comment: "Initialize Chroma as a persistent vector store with the documents, embedding model, and persist directory" and add this code snippet:
   
    ```python
    # Initialize Chroma (persistent)
    self.chroma_store = Chroma.from_documents(
        documents, self.embedding_model, persist_directory=self.persist_directory
    )
    ```
   
    This code creates a Chroma vector store using the same documents and embedding model, but also specifies a persistence directory where Chroma will store its data on disk.
   
    **Step 1.5**. Find the TODO comment: "Persist the Chroma store to disk" and add this code snippet:
   
    ```python
    self.chroma_store.persist()
    ```
   
    This code calls the persist() method on the Chroma store to ensure the data is written to disk, which is a critical step to prevent data loss.
   
    **Step 1.6**. Find the TODO comment: "Print a confirmation message with the number of documents indexed" and add this code snippet:
   
    ```python
    print(f"Initialized vector stores with {len(documents)} documents")
    ```
   
    This code prints a confirmation message showing how many documents were successfully indexed in both vector stores.


2. Next, we'll implement the `add_documents` method. This method adds new documents to existing vector stores or creates new ones if needed. 

    **Step 2.1**. Find the TODO comment: "Task 4b - Add new documents to existing vector stores" and follow the steps below.
    
    **Step 2.2**. Find the TODO comment: "Check if the documents list is empty and return early if it is" and add this code snippet:
    
    ```python
    if not documents:
        return
    ```
    
    This code checks if the documents list is empty and returns immediately if it is, avoiding unnecessary processing.
    
    **Step 2.3**. Find the TODO comment: "Add documents to the FAISS store if it exists, otherwise create a new FAISS store" and add this code snippet:
    
    ```python
    # Add to FAISS
    if self.faiss_store is not None:
        self.faiss_store.add_documents(documents)
    else:
        self.faiss_store = FAISS.from_documents(documents, self.embedding_model)
    ```
    
    This code checks if the FAISS store already exists. If it does, it adds the new documents to it; otherwise, it creates a new FAISS store from the documents. The FAISS store is kept entirely in-memory.
    
    **Step 2.4**. Find the TODO comment: "Add documents to the Chroma store if it exists, otherwise create a new Chroma store" and add this code snippet:
    
    ```python
    # Add to Chroma
    if self.chroma_store is not None:
        self.chroma_store.add_documents(documents)
    else:
        self.chroma_store = Chroma.from_documents(
            documents,
            self.embedding_model,
            persist_directory=self.persist_directory,
        )
    ```
    
    This code follows the same pattern for the Chroma store - if it exists, it adds documents to it; otherwise, it creates a new Chroma store with the specified persistence directory.
    
    **Step 2.5**. Find the TODO comment: "Persist the Chroma store to disk after adding documents" and add this code snippet:
    
    ```python
    self.chroma_store.persist()
    ```
    
    This code calls the `persist()` method on the Chroma store to ensure changes are written to disk, which is a crucial step for maintaining the Chroma database.



3. Implement the `query_stores` method. Here's where you'll create the logic to query both vector stores and compare their results. 
   
    We'll create an empty dictionary to store the results from both stores. We'll wrap the call to `similarity_search()` with time measurements using `time.time()` before and after for both the FAISS and the Chroma queries. Store both the retrieved documents and the retrieval time in the results dictionary. This will be valuable for performance analysis. The `top_k` parameter controls how many documents to retrieve - typically a value around 4 works well for RAG applications. Measuring and storing the retrieval times alongside the documents allows your system to provide insights into the performance characteristics of different vector store implementations, which can help users make informed decisions about which one to use for different scenarios.

    **Step 3.1**. Find the TODO comment: "Task 4c - Query both vector stores and compare their results" and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "Create an empty dictionary to store results from both vector stores" and add this code snippet:
    
    ```python
    results = {}
    ```
    
    This code initializes an empty dictionary that will store the query results from both vector stores.
    
    **Step 3.3**. Find the TODO comment: "Query the FAISS store if it exists, measuring retrieval time" and add this code snippet:
    
    ```python
    # Query FAISS
    if self.faiss_store is not None:
        faiss_start = time.time()
        results["faiss"] = {
            "documents": self.faiss_store.similarity_search(query, k=top_k),
            "retrieval_time": time.time() - faiss_start,
        }
    ```
    
    This code checks if the FAISS store exists, and if so, measures the time it takes to perform a similarity search. It stores both the retrieved documents and the retrieval time in the results dictionary.
    
    **Step 3.4**. Find the TODO comment: "Query the Chroma store if it exists, measuring retrieval time" and add this code snippet:
    
    ```python
    # Query Chroma
    if self.chroma_store is not None:
        chroma_start = time.time()
        results["chroma"] = {
            "documents": self.chroma_store.similarity_search(query, k=top_k),
            "retrieval_time": time.time() - chroma_start,
        }
    ```
    
    This code does the same for the Chroma store - it checks if it exists, measures the query time, and stores both the documents and retrieval time in the results dictionary.
    
    **Step 3.5**. Find the TODO comment: "Return a dictionary with results from both stores" and add this code snippet:
    
    ```python
    return results
    ```
    
    This code returns the dictionary containing the query results from both vector stores, allowing you to compare their performance and results.


4. Implement the `get_retriever` method in your code file. 
   
   This method creates a standardized retriever interface for a specified vector store. We'll check which store the user requested and verify that the store exists before returning its retriever with appropriate search parameters (setting `k=4` for the number of documents to retrieve). This method creates a consistent interface that higher-level code can use without worrying about the details of each vector store implementation. The consistent `k=4` parameter ensures that retrieval behavior is comparable across different stores.

    **Step 4.1**. Find the TODO comment: "Task 4d - Create a standardized retriever interface for a specified vector store" and follow the steps below.
   
    **Step 4.2**. Find the TODO comment: "Check if the requested store is FAISS and return its retriever if available" and add this code snippet:
   
    ```python
    if store_name.lower() == "faiss" and self.faiss_store is not None:
        return self.faiss_store.as_retriever(search_kwargs={"k": 4})
    ```
   
    This code checks if the user requested the FAISS store (converting to lowercase for case-insensitive matching) and if it exists, then returns its retriever configured to retrieve 4 documents.
   
    **Step 4.3**. Find the TODO comment: "Check if the requested store is Chroma and return its retriever if available" and add this code snippet:
   
    ```python
    elif store_name.lower() == "chroma" and self.chroma_store is not None:
        return self.chroma_store.as_retriever(search_kwargs={"k": 4})
    ```
   
    This code checks if the user requested the Chroma store and if it exists, then returns its retriever also configured to retrieve 4 documents.
   
    **Step 4.4**. Find the TODO comment: "Raise an error if the requested store is not available" and add this code snippet:
   
    ```python
    else:
        raise ValueError(f"Vector store '{store_name}' is not available")
    ```
   
    This code raises a ValueError with a clear message if the requested store doesn't exist or isn't recognized, explaining what went wrong.


The vector store manager is the heart of your system's retrieval capabilities. By implementing both FAISS and Chroma stores, you get to experience the trade-offs between different approaches:

- **FAISS**: Implemented as an in-memory only store in this application. This means it's typically faster for retrieval operations but will need to be rebuilt each time the application restarts. No .pkl file is created or used for persistence.

- **Chroma**: Implemented as a persistent store that saves its data to disk in the chroma_db directory. This allows it to maintain its state between application restarts but may have different performance characteristics compared to the in-memory FAISS store.

This dual approach allows you to compare both implementations and understand the trade-offs between speed and persistence in vector store design.



### Task 5: Create the RAG Application Interface (20 minutes)

In this task, you'll implement the main application functionality that connects all components into a cohesive RAG system.

1. Open `app.py` in your code editor and implement the `add_documents` method.
   
   This method serves as the central document ingestion pipeline for your RAG system. You'll process the raw documents into appropriate chunks using the document processor you implemented earlier. Documents are split into chunks while preserving metadata. Processed documents are added to the internal tracking list, which is important for features like reloading vector stores. When adding documents, if the FAISS store doesn't exists in the vector store manager yet, initialize both vector stores. If stores already exist, simply add the new documents to them. This approach handles both initial loading and incremental updates elegantly. The method doesn't return anything since its purpose is to modify the internal state of the RAG system.

    **Step 1.1**. Find the TODO comment: "Task 5a - Add documents document ingestion pipeline" and follow the steps below.
   
    **Step 1.2**. Find the TODO comment: "Process documents using the document processor (split into chunks, preserve metadata)" and add this code snippet:
   
    ```python
    # Process documents (split into chunks, preserve metadata)
    processed_docs = self.doc_processor.process_documents(documents)
    ```
   
    This code uses the document processor to split the input documents into appropriate chunks while preserving their metadata.
   
    **Step 1.3**. Find the TODO comment: "Add the processed documents to the tracking list" and add this code snippet:
   
    ```python
    # Add to tracking list
    self.documents.extend(processed_docs)
    ```
   
    This code adds the processed documents to the internal tracking list, which is crucial for features like reloading vector stores.
   
    **Step 1.4**. Find the TODO comment: "Add documents to vector stores (initialize if first time, otherwise add to existing)" and add this code snippet:
   
    ```python
    # Add to vector stores
    if not self.vector_store_manager.faiss_store:
        # First time adding documents, initialize vector stores
        self.vector_store_manager.initialize_stores(processed_docs)
    else:
        # Add to existing vector stores
        self.vector_store_manager.add_documents(processed_docs)
    ```
   
    This code checks if this is the first time adding documents by seeing if the FAISS store exists. If it doesn't exist yet, it initializes both vector stores. If stores already exist, it simply adds the new documents to them.

2. Next, we'll implement the `query` method.
   
   This is the central method that users will interact with most often. It checks to see  if the question is a special command (starting with "/") and, if it is, routes it to the `_handle_command` method. It also checks if the user requested a comparison between vector stores (when `vector_store` is "both") and use the `compare_vector_stores` method in that case. For normal queries, we get the appropriate retriever from the vector store manager based on the requested store name. A prompt template instructs the LLM to answer based only on the provided context. This is a key factor for grounding the model's responses in the retrieved documents. Then, create a chain that connects the LLM, retriever, and prompt. We'll provide attribution handle the response based on whether streaming is enabled. This method orchestrates the entire RAG process from query to response.

    **Step 2.1**. Find the TODO comment: "Task 5b - Implement central method for user interaction" and follow the steps below.
   
    **Step 2.2**. Find the TODO comment: "Check if the question is a special command and handle it appropriately" and add this code snippet:
   
    ```python
    # Check for special commands
    if question.startswith("/"):
        return self._handle_command(question)
    ```
   
    This code checks if the user's question starts with a slash character, which indicates a special command, and routes it to the `_handle_command` method if so.
   
    **Step 2.3**. Find the TODO comment: "If vector_store is 'both', use the compare_vector_stores method" and add this code snippet:
   
    ```python
    if vector_store.lower() == "both":
        return self.compare_vector_stores(question)
    ```
   
    This code checks if the user requested a comparison between vector stores (when `vector_store` is "both") and uses the `compare_vector_stores` method in that case.
   
    **Step 2.4**. Find the TODO comment: "Get the appropriate retriever from the vector store manager" and add this code snippet:
   
    ```python
    # Get the appropriate retriever
    retriever = self.vector_store_manager.get_retriever(vector_store)
    ```
   
    This code gets the appropriate retriever from the vector store manager based on the requested store name.
   
    **Step 2.5**. Find the TODO comment: "Create a prompt template with instructions for using context and attribution" and add this code snippet:
   
    ```python
    # Create a template with instructions for source attribution
    prompt_template = """
    Answer the question based only on the following context. If you don't know the answer, 
    just say that you don't know, don't try to make up an answer.
    
    Context:
    {context}
    
    Question: {question}
    """
   
    # Create a proper PromptTemplate
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    ```
   
    This code creates a prompt template that instructs the LLM to answer based only on the provided context, which is crucial for grounding the model's responses in the retrieved documents.
   
    **Step 2.6**. Find the TODO comment: "Create a RetrievalQA chain with the LLM, retriever, and prompt" and add this code snippet:
   
    ```python
    # Create a RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=EnhancedLLM(
            model_name=self.llm.model_name, temperature=self.llm.temperature
        ),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    ```
   
    This code sets up a `RetrievalQA` chain that connects the LLM, retriever, and prompt. The `return_source_documents=True` parameter ensures that source attribution can be provided.
   
    **Step 2.7**. Find the TODO comment: "Execute the chain with the user's question" and add this code snippet:
   
    ```python
    # Execute the chain
    chain_response = qa_chain({"query": question})
    ```
   
    This code executes the chain, passing the user's question as the "query" parameter.
   
    **Step 2.8**. Find the TODO comment: "Format the response with source attribution (handling streaming differently)" and add this code snippet:
   
    ```python
    # If streaming, we need to handle source documents separately
    if streaming:
        print("\n\nSources:\n")
        formatted_sources = self._format_source_info(
            chain_response["source_documents"]
        )
        print(formatted_sources)
        return formatted_sources
    else:
        # Format response with sources
        full_response = self._format_response_with_sources(
            chain_response["result"], chain_response["source_documents"]
        )
        return full_response
    ```
   
    This code handles the response differently based on whether streaming is enabled. If streaming is enabled, it prints the sources separately after the response. If not, it formats a complete response with sources included.


3. Lastly, implement the `_format_source_info` method. 
   
   This helper method creates a readable representation of source documents for attribution. It checks for any source documents and creates an empty list to store the formatted source information and a set to track sources you've already seen (to avoid duplicates). For each document, its metadata is extracted and a unique identifier is created combining the source and source type. Duplicate sources are skipped. Source information is formatted based on the document type. Each formatted source is added to the list with a numbering system like "[1]", "[2]", etc. Finally, all the formatted sources are joined with newlines and returned as a string. This formatting ensures that users can easily trace information back to its original source, which is essential for building trust in AI-generated responses.


    **Step 3.1**. Find the TODO comment: "Task 5c - Implement helper method for source documents and attribution." and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "Check if there are no source documents and return an appropriate message" and add this code snippet:
    
    ```python
    if not source_documents:
        return "No sources found"
    ```
    
    This code checks if the source_documents list is empty and returns a simple message if there are no sources to display.
    
    **Step 3.3**. Find the TODO comment: "Create a list to store formatted source information" and "Create a set to track seen sources to avoid duplicates" and add this code snippet:
    
    ```python
    source_info = []
    seen_sources = set()
    ```
    
    This code initializes an empty list to store the formatted source information and a set to track sources you've already seen to avoid duplicates.
    
    **Step 3.4**. Find the TODO comment: "For each document, extract metadata and format based on source type" and add this code snippet:
    
    ```python
    for i, doc in enumerate(source_documents):
        metadata = doc.metadata
        source = metadata.get("source", "Unknown")
    
        # Create a unique identifier for this source
        source_type = metadata.get("source_type", "Unknown")
        source_id = f"{source}:{source_type}"
    
        # Only include each source once
        if source_id in seen_sources:
            continue
        seen_sources.add(source_id)
    ```
    
    This code loops through each document, extracts its metadata, creates a unique identifier for each source, and skips sources that have already been processed to avoid duplication.
    
    **Step 3.5**. Find the TODO comment: "Handle different source types (PDF, web, wikibook, CSV) with appropriate formatting" and add this code snippet:
    
    ```python
        # Format source information based on type
        if source_type == "pdf":
            page = metadata.get("page", "Unknown")
            source_info.append(f"[{i+1}] PDF: {source} (Page {page})")
        elif source_type == "web":
            source_info.append(f"[{i+1}] Web: {source}")
        elif source_type == "wikibook":
            section = metadata.get("section", "Unknown")
            title = metadata.get("title", "Unknown")
            source_info.append(
                f"[{i+1}] WikiBook: {title}, Section {section} ({source})"
            )
        elif source_type == "csv":
            row = metadata.get("row", "Unknown")
            source_info.append(f"[{i+1}] CSV: {source} (Row {row})")
        else:
            source_info.append(f"[{i+1}] {source}")
    ```
    
    This code formats the source information differently based on the document type: for PDFs, it includes the page number; for web pages, it shows just the URL; for WikiBooks, it includes the title and section; and for CSV files, it includes the row if available.
    
    **Step 3.6**. Find the TODO comment: "Join all formatted source information with newlines and return" and add this code snippet:
    
    ```python
    return "\n".join(source_info)
    ```
    
    This code joins all the formatted sources with newlines and returns the resulting string, making it easy for users to trace information back to its original source.

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
