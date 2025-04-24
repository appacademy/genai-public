from typing import Dict, List, Any, Optional, Callable


class Document:
    """
    A simple document class to replace LangChain's Document.
    Contains text content and associated metadata.
    """

    def __init__(self, page_content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a document with content and metadata.

        Args:
            page_content: The text content of the document.
            metadata: Optional metadata associated with the document.
        """
        self.page_content = page_content
        self.metadata = metadata or {}


def split_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: List[str] = ["\n\n", "\n", ". ", " ", ""],
) -> List[str]:
    """
    Split text into chunks using a list of separators.

    Args:
        text: The text to split.
        chunk_size: The target size of each chunk.
        chunk_overlap: The overlap between chunks.
        separators: The separators to use for splitting, in order of preference.

    Returns:
        A list of text chunks.
    """
    # If the text is already smaller than the chunk size, return it as is
    if len(text) <= chunk_size:
        return [text]

    # Ensure chunk_overlap is less than chunk_size to prevent infinite loops
    chunk_overlap = min(chunk_overlap, chunk_size - 1)

    chunks = []
    start = 0
    previous_start = -1  # To detect if we're making progress

    while start < len(text):
        # Safety check: ensure we're making progress
        if start <= previous_start:
            # Force progress by advancing at least one character
            start = previous_start + 1

        previous_start = start

        # Find the end of the chunk
        end = min(start + chunk_size, len(text))

        # If we're not at the end of the text, try to find a good separator
        if end < len(text):
            # Try each separator in order
            separator_found = False
            for separator in separators:
                if separator == "":  # Last resort: just split at the chunk size
                    break

                # Find the last occurrence of the separator within the chunk
                last_separator = text.rfind(separator, start, end)

                if (
                    last_separator != -1 and last_separator > start
                ):  # Ensure we're making progress
                    # Found a separator, use it as the end point
                    end = last_separator + len(separator)
                    separator_found = True
                    break

            # If no good separator was found and we're using the empty string separator,
            # ensure we're making progress by using the original end
            if not separator_found and end <= start:
                end = start + 1  # Ensure at least one character is included

        # Extract the chunk and add it to the list
        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)

        # Move the start pointer for the next chunk, accounting for overlap
        new_start = end - chunk_overlap

        # Ensure we're making progress
        if new_start <= start:
            new_start = start + 1

        start = new_start

    return chunks


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: List[str] = ["\n\n", "\n", ". ", " ", ""],
) -> List[Document]:
    """
    Split a list of documents into chunks.

    Args:
        documents: The documents to split.
        chunk_size: The target size of each chunk.
        chunk_overlap: The overlap between chunks.
        separators: The separators to use for splitting, in order of preference.

    Returns:
        A list of document chunks.
    """
    splits = []

    for doc in documents:
        # Split the text
        text_chunks = split_text(
            doc.page_content, chunk_size, chunk_overlap, separators
        )

        # Create a new Document for each chunk with the same metadata
        for i, chunk in enumerate(text_chunks):
            # Create a copy of the metadata
            chunk_metadata = doc.metadata.copy()
            # Add chunk index to metadata
            chunk_metadata["chunk_index"] = i

            # Create a new Document
            splits.append(Document(page_content=chunk, metadata=chunk_metadata))

    return splits
