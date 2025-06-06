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
    # Create the LLM
    llm = create_llm(temperature=0.5)  # Lower temperature for more factual summaries

    # Create the prompt template
    prompt = PromptTemplate.from_template(
        """
        Below is a news article. Please provide a concise summary in 3-4 sentences.
        Focus on the main points and key information.
        
        ARTICLE:
        Title: {title}
        
        Description: {description}
        
        Content: {content}
        
        SUMMARY:
        """
    )

    # Create the chain
    chain = prompt | llm | StrOutputParser()

    # Add preprocessing to handle different input formats
    def preprocess_input(data: Union[Dict[str, Any], ArticleInput]) -> Dict[str, Any]:
        """Preprocess the input to ensure it has the expected format."""
        if isinstance(data, ArticleInput):
            return {
                "title": data.title,
                "description": data.description or "",
                "content": data.content or "",
            }

        # Handle dictionary input
        return {
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "content": data.get("content", ""),
        }

    # Add preprocessing to the chain
    return RunnableLambda(preprocess_input) | chain


def create_categorization_chain():
    """
    Create a chain for categorizing news articles.

    Returns:
        LangChain chain for article categorization
    """
    # Create the LLM
    llm = create_llm(
        temperature=0.3
    )  # Lower temperature for more consistent categorization

    # Create the prompt template
    prompt = PromptTemplate.from_template(
        """
        Categorize the following news article into exactly one of these categories:
        {categories}
        
        ARTICLE:
        Title: {title}
        
        Description: {description}
        
        INSTRUCTIONS:
        1. Return ONLY the category name, with no additional text, explanation, or reasoning
        2. The category must be one of the exact options listed above
        3. Do not include any spaces before or after the category name
        
        CATEGORY:
        """
    )

    # Create the chain
    chain = prompt | llm | StrOutputParser()

    # Add preprocessing and validation
    def preprocess_and_validate(
        data: Union[Dict[str, Any], ArticleInput],
    ) -> Dict[str, Any]:
        """Preprocess the input and add validation logic."""
        # Extract article data
        if isinstance(data, ArticleInput):
            article_data = {
                "title": data.title,
                "description": data.description or "",
                "categories": ", ".join(config.VALID_CATEGORIES),
            }
        else:
            article_data = {
                "title": data.get("title", ""),
                "description": data.get("description", ""),
                "categories": ", ".join(config.VALID_CATEGORIES),
            }

        return article_data

    # Add post-processing to validate the category
    def validate_category(category: str) -> Dict[str, Any]:
        """Validate that the category is in the list of valid categories."""
        category = category.strip().lower()

        if category not in config.VALID_CATEGORIES:
            logger.warning(
                f"LLM returned invalid category: {category}. Defaulting to 'general'."
            )
            return {"category": "general", "confidence": 0.0}

        return {"category": category, "confidence": 1.0}

    # Combine preprocessing, chain, and validation
    return (
        RunnableLambda(preprocess_and_validate)
        | chain
        | RunnableLambda(validate_category)
    )


def create_multi_processing_chain():
    """
    Create a chain that performs both summarization and categorization.

    Returns:
        LangChain chain for combined article processing
    """
    # Create the individual chains
    summarization_chain = create_summarization_chain()
    categorization_chain = create_categorization_chain()

    # Define the combined chain
    def process_article(data: Union[Dict[str, Any], ArticleInput]) -> Dict[str, Any]:
        """Process an article with both summarization and categorization."""
        # Run summarization
        summary = summarization_chain.invoke(data)

        # Run categorization
        category_result = categorization_chain.invoke(data)

        # Combine results
        return {
            "title": (
                data.title if isinstance(data, ArticleInput) else data.get("title", "")
            ),
            "summary": summary,
            "category": category_result["category"],
            "confidence": category_result.get("confidence", 1.0),
        }

    return RunnableLambda(process_article)


# Create singleton instances of the chains for reuse
summarization_chain = create_summarization_chain()
categorization_chain = create_categorization_chain()
multi_processing_chain = create_multi_processing_chain()
