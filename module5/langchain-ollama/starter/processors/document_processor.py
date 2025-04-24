"""
Document Processor for RAG System

This module provides functionality for loading and processing documents from various sources,
including PDFs, web pages, and CSV files. It handles document chunking and metadata management.
"""

import os
import uuid
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter,
)
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, CSVLoader
from bs4 import BeautifulSoup
import requests


class DocumentProcessor:
    """
    Handles loading and processing documents from various sources.

    This class provides methods for loading documents from PDFs, web pages, and CSV files,
    as well as processing them into chunks suitable for embedding and retrieval.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor.

        Args:
            chunk_size: The size of text chunks for splitting documents. Defaults to 1000.
            chunk_overlap: The overlap between chunks. Defaults to 200.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize text splitters
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        self.markdown_splitter = MarkdownTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def load_pdf(self, file_path: str) -> List[Document]:
        """
        Load a PDF file and extract its content.

        Args:
            file_path: The path to the PDF file.

        Returns:
            A list of Document objects, one per page.
        """
        # Use PyPDFLoader to load the PDF file
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Add metadata to each document
        for doc in documents:
            if not doc.metadata:
                doc.metadata = {}

            # Add source information
            doc.metadata["source"] = os.path.basename(file_path)
            doc.metadata["source_type"] = "pdf"
            doc.metadata["file_path"] = file_path

            # Add a unique ID
            doc.metadata["doc_id"] = str(uuid.uuid4())

        return documents

    def load_web_page(self, url: str) -> List[Document]:
        """
        Load content from a web page.

        Args:
            url: The URL of the web page.

        Returns:
            A list of Document objects containing the web page content.
        """
        # Use WebBaseLoader to load the web page
        loader = WebBaseLoader(url)
        documents = loader.load()

        # Add metadata to each document
        for doc in documents:
            if not doc.metadata:
                doc.metadata = {}

            # Add source information
            doc.metadata["source"] = url
            doc.metadata["source_type"] = "web"

            # Add a unique ID
            doc.metadata["doc_id"] = str(uuid.uuid4())

        return documents

    def load_wikibook(self, url: str, max_pages: int = 10) -> List[Document]:
        """
        Load and process a WikiBook with specialized handling, including following links to subpages.

        Args:
            url: The URL of the WikiBook.
            max_pages: Maximum number of pages to load (to prevent excessive crawling).

        Returns:
            A list of Document objects, one per section.
        """
        try:
            # Initialize variables
            documents = []
            visited_urls = set()
            urls_to_visit = [url]
            base_url = "https://en.wikibooks.org"
            page_count = 0
            
            # Extract the book name from the URL
            book_name = url.split("/")[-1]
            
            # Process pages until we've visited all URLs or reached the maximum
            while urls_to_visit and page_count < max_pages:
                current_url = urls_to_visit.pop(0)
                
                # Skip if we've already visited this URL
                if current_url in visited_urls:
                    continue
                
                # Mark as visited
                visited_urls.add(current_url)
                page_count += 1
                
                print(f"  -> Processing WikiBook page {page_count}/{max_pages}: {current_url}")
                
                try:
                    # Fetch the page content
                    response = requests.get(current_url, timeout=30) # Added timeout
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Extract the title
                    title_element = soup.find("h1", {"id": "firstHeading"})
                    title = title_element.text.strip() if title_element else book_name.replace("_", " ") # Use book name as fallback title
                    
                    # Find the main content area
                    content_div = soup.find("div", {"id": "mw-content-text"})
                    if not content_div:
                        print(f"  -> Could not find main content div for {current_url}")
                        continue
                    
                    # Remove known non-content elements (e.g., navigation boxes, edit links)
                    for element_type, attrs in [
                        ("table", {"class": "navbox"}),
                        ("div", {"class": "printfooter"}),
                        ("div", {"id": "catlinks"}),
                        ("span", {"class": "mw-editsection"}),
                    ]:
                        for element in content_div.find_all(element_type, attrs):
                            element.decompose()
                    
                    # Extract all text from the main content area
                    page_text = content_div.get_text(separator="\n", strip=True)
                    
                    if page_text:
                        # Create one document per page
                        doc = Document(
                            page_content=page_text,
                            metadata={
                                "source": current_url,
                                "source_type": "wikibook",
                                "title": title,
                                "doc_id": str(uuid.uuid4()),
                            },
                        )
                        documents.append(doc)
                    else:
                        print(f"  -> No text content extracted from {current_url}")

                    # Find links to other pages in the same book (only from the main page)
                    if page_count == 1:
                        for link in content_div.find_all("a", href=True):
                            href = link["href"]
                            # Check if it's a relative link within the same book
                            if href.startswith(f"/wiki/{book_name}/") and ":" not in href:
                                full_url = base_url + href
                                if full_url not in visited_urls and full_url not in urls_to_visit:
                                    urls_to_visit.append(full_url)
                            # Check if it's an absolute link within the same book (less common)
                            elif href.startswith(f"{base_url}/wiki/{book_name}/") and ":" not in href:
                                if href not in visited_urls and href not in urls_to_visit:
                                     urls_to_visit.append(href)

                except requests.exceptions.RequestException as req_err:
                    print(f"  -> Request error processing {current_url}: {req_err}")
                except Exception as parse_err:
                    print(f"  -> Error parsing content from {current_url}: {parse_err}")

            print(f"  -> Processed {page_count} pages from WikiBook '{book_name}', created {len(documents)} documents.")
            return documents
        
        except Exception as e:
            print(f"Error initiating WikiBook processing for {url}: {e}")
            print("Falling back to standard web page loading")
            return self.load_web_page(url)

    def load_csv(self, file_path: str, content_column: str) -> List[Document]:
        """
        Load data from a CSV file.

        Args:
            file_path: The path to the CSV file.
            content_column: The name of the column containing the content to use.

        Returns:
            A list of Document objects, one per row.
        """
        try:
            # Try the current LangChain approach
            loader = CSVLoader(
                file_path, csv_args={"delimiter": ","}, column_name=content_column
            )
            documents = loader.load()
        except TypeError:
            # Fall back to the alternative approach for older versions
            loader = CSVLoader(file_path, csv_args={"delimiter": ","})
            if hasattr(loader, "set_column"):
                loader.set_column(content_column)
            documents = loader.load()

        # Add metadata to each document
        for doc in documents:
            if not doc.metadata:
                doc.metadata = {}

            # Add source information
            doc.metadata["source"] = os.path.basename(file_path)
            doc.metadata["source_type"] = "csv"
            doc.metadata["file_path"] = file_path

            # Add a unique ID
            doc.metadata["doc_id"] = str(uuid.uuid4())

        return documents

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks and ensure metadata is preserved.

        Args:
            documents: A list of Document objects to process.

        Returns:
            A list of processed Document chunks.
        """
        processed_docs = []

        for doc in documents:
            # Store original metadata
            original_metadata = doc.metadata if doc.metadata else {}

            # Use recursive character splitter for all document types now
            chunks = self.text_splitter.split_documents([doc])

            # Ensure metadata is preserved in each chunk
            for chunk in chunks:
                if not chunk.metadata:
                    chunk.metadata = {}

                # Merge original metadata with any new metadata
                for key, value in original_metadata.items():
                    if key not in chunk.metadata:
                        chunk.metadata[key] = value

                # Ensure each chunk has a unique ID
                if "doc_id" not in chunk.metadata:
                    chunk.metadata["doc_id"] = str(uuid.uuid4())

                processed_docs.append(chunk)

        return processed_docs
