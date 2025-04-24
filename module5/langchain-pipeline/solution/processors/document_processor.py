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
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Add source metadata
        file_name = os.path.basename(file_path)
        for doc in documents:
            if not doc.metadata:
                doc.metadata = {}
            doc.metadata["source"] = file_name
            doc.metadata["source_type"] = "pdf"
            doc.metadata["file_path"] = file_path
            # Add unique ID for each document chunk
            doc.metadata["doc_id"] = str(uuid.uuid4())

        return documents

    def load_web_page(self, url: str) -> List[Document]:
        """Load content from a web page."""
        loader = WebBaseLoader(url)
        documents = loader.load()

        # Add source metadata
        for doc in documents:
            if not doc.metadata:
                doc.metadata = {}
            doc.metadata["source"] = url
            doc.metadata["source_type"] = "web"
            # Add unique ID for each document chunk
            doc.metadata["doc_id"] = str(uuid.uuid4())

        return documents

    def load_wikibook(self, url: str) -> List[Document]:
        """Load and process a WikiBook with better content extraction."""
        try:
            # Fetch the content
            response = requests.get(url)
            response.raise_for_status()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the title
            title = soup.find("h1", {"id": "firstHeading"}).text.strip()

            # Extract the main content
            content_div = soup.find("div", {"id": "mw-content-text"})

            # Remove unwanted elements
            for unwanted in content_div.select(
                ".navbox, .vertical-navbox, .ambox, .mbox-small, .noprint, .mw-empty-elt"
            ):
                unwanted.decompose()

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

        except Exception as e:
            print(f"Error loading WikiBook from {url}: {str(e)}")
            # Fallback to standard WebBaseLoader
            print("Falling back to standard WebBaseLoader")
            return self.load_web_page(url)

    def load_csv(self, file_path: str, content_column: str) -> List[Document]:
        """Load documents from a CSV file."""
        # Updated to be compatible with current LangChain version
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

        return documents

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks and ensure metadata is preserved."""
        processed_docs = []

        for doc in documents:
            # Store original metadata
            original_metadata = doc.metadata if doc.metadata else {}

            # Choose the appropriate splitter based on source type
            splitter = (
                self.markdown_splitter
                if original_metadata.get("source_type") == "wikibook"
                else self.text_splitter
            )

            # Split the document
            chunks = splitter.split_documents([doc])

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
