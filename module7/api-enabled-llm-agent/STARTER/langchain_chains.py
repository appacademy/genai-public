"""
LangChain chains for the NewsAgent application.
Defines chain compositions for API interactions and LLM operations.
"""

import logging
from typing import Dict, Any, List, Optional, Union
import os
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.llms.ollama import Ollama
from pydantic import BaseModel, Field

import config
from ollama_client import OllamaClient

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")


class ArticleInput(BaseModel):
    """Input schema for article processing chains."""

    title: str = Field(description="The title of the article")
    description: Optional[str] = Field(
        default="", description="The description or subtitle of the article"
    )
    content: Optional[str] = Field(
        default="", description="The main content of the article"
    )
    source: Optional[str] = Field(default="", description="The source of the article")
    published_at: Optional[str] = Field(
        default="", description="The publication date of the article"
    )


class CategoryOutput(BaseModel):
    """Output schema for article categorization."""

    category: str = Field(description="The category of the article")
    confidence: Optional[float] = Field(
        default=None, description="Confidence score for the categorization"
    )


def create_llm(temperature: float = 0.7, model: str = "gemma3:4b"):
    """
    Create a LangChain LLM instance configured for Ollama.

    Args:
        temperature: Temperature parameter for the LLM (default: 0.7)
        model: Model name to use (default: "gemma3:4b")

    Returns:
        Configured Ollama LLM instance
    """
    return Ollama(model=model, base_url=OLLAMA_API_URL, temperature=temperature)


def create_summarization_chain():
    """
    Create a chain for summarizing news articles.

    Returns:
        LangChain chain for article summarization
    """
    # TODO: Implement a LangChain chain for article summarization

    # TODO: Create an LLM with appropriate temperature for factual summarization

    # TODO: Design a prompt template for article summarization

    # TODO: Create the chain by composing: prompt | llm | StrOutputParser()

    # TODO: Add preprocessing logic to handle different input formats

    # TODO: Return the complete chain with preprocessing


def create_categorization_chain():
    """
    Create a chain for categorizing news articles.

    Returns:
        LangChain chain for article categorization
    """
    # TODO: Implement a LangChain chain for article categorization

    # TODO: Create an LLM with appropriate temperature for consistent categorization

    # TODO: Design a prompt template with clear instructions for categorization

    # TODO: Create the base chain: prompt | llm | StrOutputParser()

    # TODO: Add preprocessing to format the input for the prompt

    # TODO: Add post-processing to validate that categories match allowed values

    # TODO: Combine the preprocessing, chain, and post-processing


def create_multi_processing_chain():
    """
    Create a chain that performs both summarization and categorization.

    Returns:
        LangChain chain for combined article processing
    """
    # TODO: Implement a LangChain chain that combines multiple operations

    # TODO: Reuse the previously created chains

    # TODO: Create a processing function

    # TODO: Combine the results

    # TODO: Return the combined chain


# Create singleton instances of the chains for reuse
summarization_chain = create_summarization_chain()
categorization_chain = create_categorization_chain()
multi_processing_chain = create_multi_processing_chain()
