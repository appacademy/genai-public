"""
Document Processor Module

This module handles loading and processing documents from various sources:
- PDF files
- Web pages
- WikiBooks
- CSV files

It includes specialized processing for different document types and ensures
metadata is preserved during document splitting.
"""

import os
import uuid
import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter,
)
from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    CSVLoader,
    TextLoader,
)


class DocumentProcessor:
    """Handles loading and processing documents from various sources."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        # Create a specialized splitter for markdown content (like WikiBooks)
        self.markdown_splitter = MarkdownTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

    def load_pdf(self, file_path: str) -> List[Document]:
        """Load documents from a PDF file."""
        # TODO: Task 2b - Implement PDF Loading and Processing
        # TODO: Use PyPDFLoader to load the PDF file

        # TODO: Add appropriate metadata to each document (source, source_type, file_path)

        # TODO: Add a unique ID for each document

        return documents

    def load_web_page(self, url: str) -> List[Document]:
        """Load content from a web page."""
        # TODO: Task 2c - Implement Web Page Loading and Processing
        # TODO: Use WebBaseLoader to load content from the URL

        # TODO: Add appropriate metadata to each document (source, source_type)

        # TODO: Add a unique ID for each document

        return documents

    def load_wikibook(self, url: str) -> List[Document]:
        """Load and process a WikiBook with better content extraction."""
        # TODO: Task 2a - Implement Webscraping, Loading, and Processing
        # TODO: Implement specialized WikiBook scraping using BeautifulSoup

        # TODO: Extract the title and main content from the WikiBook

        # TODO: Process the content by sections with headings

        # TODO: Create Document objects with appropriate metadata

        # TODO: Include error handling with fallback to standard web page loading

    def load_csv(self, file_path: str, content_column: str) -> List[Document]:
        """Load documents from a CSV file."""
        # TODO: Task 2d - Implement CSV Loading and Processing
        # TODO: Use CSVLoader to load data from the CSV file

        # TODO: Add appropriate metadata to each document

        # TODO: Return the processed documents

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks and ensure metadata is preserved."""
        # TODO: Task 2e - Implement Document Chunking
        # TODO: Create a list to store processed document chunks

        # TODO: For each document, select the appropriate text splitter based on document type

        # TODO: Split the document into chunks using the selected splitter

        # TODO: Ensure all metadata from the original document is preserved in each chunk

        # TODO: Add unique IDs to each chunk if not already present

        # TODO: Return the processed document chunks
