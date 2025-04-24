"""
LangChain Integration Module

This module provides custom LangChain-compatible classes for embeddings and LLMs:
- EnhancedHuggingFaceEmbeddings: A LangChain embeddings class that uses HuggingFace for embeddings
- EnhancedLLM: A placeholder LLM class that will be replaced with Gemma 3/Ollama integration
"""

import os
import warnings
import time
from typing import Any, Dict, List, Mapping, Optional, Union
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import GenerationChunk
from pydantic import Field
import numpy as np

# Suppress deprecation warnings for a cleaner console UI
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="USER_AGENT environment variable not set")
warnings.filterwarnings(
    "ignore",
    message="Default values for EnhancedHuggingFaceEmbeddings.model_name were deprecated",
)

# Set environment variables to suppress warnings
os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"
os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# Import HuggingFace libraries
from langchain_community.embeddings import HuggingFaceEmbeddings


class EnhancedHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    """Enhanced LangChain embeddings implementation for HuggingFace models."""

    # TODO: Task 3a - Implement and Initialize the EnhancedHuggingFaceEmbeddings class
    # TODO: Set the default model to sentence-transformers/all-MiniLM-L6-v2

    # TODO: Initialize the parent HuggingFaceEmbeddings class with the provided kwargs

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using HuggingFace.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        # TODO: Task 3b - Creating embeddings for multiple documents at once
        # TODO: Use the parent class method to embed multiple documents

    def embed_query(self, text: str) -> List[float]:
        """Embed a query using HuggingFace.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        # TODO: Task 3c - Embed user queries
        # TODO: Use the parent class method to embed a single query text


class EnhancedLLM(LLM):
    """
    Placeholder LLM implementation for the RAG pipeline.

    This is a stub implementation that will be replaced with Gemma 3/Ollama integration
    in a future activity. It provides mock responses to demonstrate the RAG pipeline
    architecture without requiring an actual LLM or API token.

    TODO: In the follow-up activity, this class will be modified to use Gemma 3 via Ollama.
    """

    model_name: str = "placeholder-model"
    temperature: float = 0.7
    max_tokens: int = 1500

    def __init__(self, **kwargs):
        """Initialize the placeholder LLM."""
        super().__init__(**kwargs)
        print("\n📢 Using placeholder LLM implementation")
        print("   This version returns mock responses and doesn't require an API token")
        print(
            "   In a future activity, this will be replaced with Gemma 3 via Ollama\n"
        )

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "placeholder_llm"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Return a mock response instead of calling an actual LLM.

        This method simulates LLM behavior by:
        1. Adding a small delay to mimic processing time
        2. Returning a placeholder response that acknowledges the query
        3. Including retrieved document information when available

        Args:
            prompt: The prompt that would be passed to the model
            stop: A list of strings to stop generation (not used in mock)
            run_manager: A callback manager (not used in mock)

        Returns:
            A mock response string
        """
        # Simulate processing time
        time.sleep(0.5)

        # Extract any document references from the prompt
        doc_info = ""
        if "Context information is below" in prompt:
            # Try to extract document sources from the prompt
            try:
                context_section = prompt.split("Context information is below")[1].split(
                    "Query:"
                )[0]
                sources = []
                for line in context_section.split("\n"):
                    if "Source:" in line:
                        sources.append(line.strip())
                if sources:
                    doc_info = "\n\nBased on these sources:\n" + "\n".join(sources)
            except:
                pass

        # Create a mock response
        response = (
            f"[Placeholder LLM Response]\n\n"
            f"I've analyzed your query about: '{prompt[:50]}...'\n\n"
            f"In a real implementation, this would be answered by Gemma 3 via Ollama."
            f"{doc_info}\n\n"
            f"To implement the actual LLM integration, you'll modify the EnhancedLLM class "
            f"in the follow-up activity."
        )

        return response

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Stream a mock response with artificial delays to simulate streaming.

        Args:
            prompt: The prompt that would be passed to the model
            stop: A list of strings to stop generation (not used in mock)
            run_manager: A callback manager (not used in mock)

        Yields:
            Chunks of the mock response with delays
        """
        # Get the full response
        full_response = self._call(prompt, stop, run_manager, **kwargs)

        # Split into sentences and yield with delays
        sentences = full_response.split(". ")
        for i, sentence in enumerate(sentences):
            # Add period back except for last sentence which might not have ended with one
            if i < len(sentences) - 1:
                sentence += "."

            # Simulate thinking time
            time.sleep(0.2)

            yield GenerationChunk(text=sentence + " ")
