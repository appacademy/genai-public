"""
LangChain tools for the NewsAgent application.
Provides tools for interacting with the News API and processing articles.
"""

import logging
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langchain_core.tools import BaseTool, ToolException
from langchain_core.callbacks import CallbackManagerForToolRun
import requests

# Import middleware components
from cache import Cache
from rate_limiter import RateLimiter
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

# Initialize Ollama client
ollama_client = OllamaClient(OLLAMA_API_URL)


# Import utility functions for enhanced terminal output
from langchain_utils import (
    print_tool_action,
    print_error,
    print_success,
    print_info,
)

# Global variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY environment variable not set")
NEWS_API_BASE_URL = config.NEWS_API_BASE_URL

# Shared articles storage
_SHARED_ARTICLES = []


# Initialize shared services
_cache = Cache(expiry_time=config.DEFAULT_CACHE_EXPIRY)
_rate_limiter = RateLimiter(config.REQUESTS_PER_MINUTE)


class NewsAPIBaseTool(BaseTool):
    """Base class for News API tools with shared functionality."""

    def __init__(self):
        """Initialize the tool."""
        super().__init__()

        # Store for articles to be used by other tools
        self._articles = []

        print_tool_action(f"Initialized {self.__class__.__name__}")

    def _make_api_request(
        self, endpoint: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make an API request with caching, rate limiting, and error handling.

        Args:
            endpoint: API endpoint
            params: Request parameters

        Returns:
            API response as dictionary
        """
        global _cache, _rate_limiter

        # Ensure API key is in params
        if "apiKey" not in params:
            params["apiKey"] = NEWS_API_KEY

        # Check if we have a cached response
        cached_data = _cache.get(endpoint, params)
        if cached_data:
            print_tool_action(f"Cache hit for {endpoint}")
            return cached_data

        # Apply rate limiting
        wait_time = _rate_limiter.wait_for_token()
        if wait_time > 0:
            print_tool_action(f"Rate limiting applied - waited {wait_time:.2f} seconds")

        # Make the API request
        print_tool_action(f"Sending request to {endpoint}")
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()

            result = response.json()

            # Cache the response
            _cache.set(endpoint, params, result)
            print_tool_action(f"Request successful - caching results")

            return result
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_msg = f"HTTP error {status_code}: {e}"

            # Handle different status codes
            if status_code == 401:
                error_msg = "Authentication error: Invalid API key"
            elif status_code == 429:
                error_msg = "Rate limit exceeded: Too many requests"
            elif status_code >= 500:
                error_msg = "Server error: News API service is experiencing issues"

            logger.error(error_msg)
            raise ToolException(error_msg)
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error: Unable to connect to News API"
            logger.error(error_msg)
            raise ToolException(error_msg)
        except requests.exceptions.Timeout:
            error_msg = "Timeout error: News API request timed out"
            logger.error(error_msg)
            raise ToolException(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            logger.error(error_msg)
            raise ToolException(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            raise ToolException(error_msg)

    def _store_articles(self, articles: List[Dict[str, Any]]) -> None:
        """Store articles for later use by other tools."""
        global _SHARED_ARTICLES
        self._articles = articles
        _SHARED_ARTICLES = articles
        print_tool_action(f"Stored {len(articles)} articles for shared access")

    @classmethod
    def get_stored_articles(cls) -> List[Dict[str, Any]]:
        """Get the stored articles from the last API call."""
        global _SHARED_ARTICLES
        return _SHARED_ARTICLES


class GetHeadlinesTool(NewsAPIBaseTool):
    """Tool for fetching top headlines from the News API."""

    name: str = "get_headlines"
    description: str = (
        "Get top headlines by category. Input should be a category name or 'all' for all categories. Valid categories are: business, entertainment, general, health, science, sports, technology."
    )

    def __init__(self):
        """Initialize the tool."""
        super().__init__()

    def get_headlines(self, category: str = "all") -> str:
        """
        Public method to fetch top headlines with optional filtering by category.

        Args:
            category: News category or 'all' (default: "all")

        Returns:
            Formatted string of headlines
        """
        return self._run(category=category)

    def _run(
        self,
        category: str = "all",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Fetch top headlines with optional filtering by category.

        Args:
            category: News category or 'all' (default: "all")
            run_manager: Callback manager for the tool run

        Returns:
            Formatted string of headlines
        """
        try:
            # Convert 'all' to None for the API
            cat = None if category.lower() == "all" else category.lower()

            # Validate category if provided
            if cat and cat not in config.VALID_CATEGORIES:
                return f"Invalid category: {category}. Valid categories are: {', '.join(config.VALID_CATEGORIES)}"

            # Set up parameters
            endpoint = f"{NEWS_API_BASE_URL}/top-headlines"
            params = {"country": config.DEFAULT_COUNTRY}

            if cat:
                params["category"] = cat

            # Make the API request
            result = self._make_api_request(endpoint, params)
            articles = result["articles"]

            # Store articles for later use
            self._store_articles(articles)

            # Format the results
            return self._format_articles(articles)

        except ToolException as e:
            return str(e)
        except Exception as e:
            logger.error(f"Error getting headlines: {e}")
            return f"Error fetching headlines: {str(e)}"

    def _format_articles(self, articles: List[Dict[str, Any]]) -> str:
        """Format articles for display."""
        if not articles:
            return "No articles found."

        result = f"Found {len(articles)} articles:\n\n"

        # Display up to 5 articles
        for i, article in enumerate(articles[:5], 1):
            result += f"{i}. {article['title']}\n"
            result += f"   Source: {article.get('source', {}).get('name', 'Unknown')}\n"
            result += f"   Published: {article.get('publishedAt', 'Unknown')}\n\n"

        if len(articles) > 5:
            result += f"... and {len(articles) - 5} more articles.\n"

        return result


class SearchNewsTool(NewsAPIBaseTool):
    """Tool for searching news articles from the News API."""

    name: str = "search_news"
    description: str = "Search for news articles. Input should be a search query."

    def __init__(self):
        """Initialize the tool."""
        super().__init__()

    def search_news(self, query: str) -> str:
        """
        Public method to search for news articles matching the given query.

        Args:
            query: Search query

        Returns:
            Formatted string of search results
        """
        return self._run(query=query)

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Search for news articles matching the given query.

        Args:
            query: Search query
            run_manager: Callback manager for the tool run

        Returns:
            Formatted string of search results
        """
        try:
            if not query.strip():
                return "Search query cannot be empty."

            # Set up parameters
            endpoint = f"{NEWS_API_BASE_URL}/everything"
            params = {"q": query}

            # Make the API request
            result = self._make_api_request(endpoint, params)
            articles = result["articles"]

            # Store articles for later use
            self._store_articles(articles)

            # Format the results
            return self._format_articles(articles)

        except ToolException as e:
            return str(e)
        except Exception as e:
            logger.error(f"Error searching news: {e}")
            return f"Error searching news: {str(e)}"

    def _format_articles(self, articles: List[Dict[str, Any]]) -> str:
        """Format articles for display."""
        if not articles:
            return "No articles found."

        result = f"Found {len(articles)} articles:\n\n"

        # Display up to 5 articles
        for i, article in enumerate(articles[:5], 1):
            result += f"{i}. {article['title']}\n"
            result += f"   Source: {article.get('source', {}).get('name', 'Unknown')}\n"
            result += f"   Published: {article.get('publishedAt', 'Unknown')}\n\n"

        if len(articles) > 5:
            result += f"... and {len(articles) - 5} more articles.\n"

        return result


class SummarizeArticleTool(NewsAPIBaseTool):
    """Tool for summarizing a news article using an LLM."""

    name: str = "summarize_article"
    description: str = (
        "Summarize a news article. Input should be the article index from the most recent headlines or search results."
    )

    def __init__(self):
        """Initialize the tool."""
        super().__init__()

    def summarize_article(self, index: str) -> str:
        """
        Public method to generate a concise summary of a news article using an LLM.

        Args:
            index: Article index (1-based)

        Returns:
            Article summary
        """
        return self._run(index=index)

    def _run(
        self, index: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Generate a concise summary of a news article using an LLM.

        Args:
            index: Article index (1-based)
            run_manager: Callback manager for the tool run

        Returns:
            Article summary
        """
        try:
            # Convert index to integer
            idx = int(index) - 1

            # Get the stored articles
            articles = self.get_stored_articles()

            # Check if we have articles and if the index is valid
            if not articles:
                return "No articles available. Please fetch headlines or search for news first."

            if idx < 0 or idx >= len(articles):
                return f"Invalid article index. Please choose between 1 and {len(articles)}."

            article = articles[idx]

            # Extract relevant information from the article
            title = article.get("title", "")
            description = article.get("description", "")
            content = article.get("content", "")

            # Combine the information for the LLM
            article_text = (
                f"Title: {title}\n\nDescription: {description}\n\nContent: {content}"
            )

            # Create a prompt for the LLM
            prompt = f"""
            Below is a news article. Please provide a concise summary in 3-4 sentences.
            Focus on the main points and key information.
            
            ARTICLE:
            {article_text}
            
            SUMMARY:
            """

            # Apply rate limiting for LLM API
            wait_time = _rate_limiter.wait_for_token()
            if wait_time > 0:
                print_tool_action(
                    f"Rate limiting applied for LLM request - waited {wait_time:.2f} seconds"
                )

            # Call the Ollama API
            ollama_response = ollama_client.generate(prompt)
            summary = ollama_response["response"].strip()

            return f"Title: {title}\nSummary: {summary}"

        except ValueError:
            return "Please provide a valid article number."
        except ToolException as e:
            return str(e)
        except Exception as e:
            logger.error(f"Error summarizing article: {e}")
            return f"Error summarizing article: {str(e)}"


class CategorizeArticleTool(NewsAPIBaseTool):
    """Tool for categorizing a news article using an LLM."""

    name: str = "categorize_article"
    description: str = (
        "Categorize a news article. Input should be the article index from the most recent headlines or search results."
    )

    def __init__(self):
        """Initialize the tool."""
        super().__init__()

    def categorize_article(self, index: str) -> str:
        """
        Public method to categorize a news article using an LLM.

        Args:
            index: Article index (1-based)

        Returns:
            Article category
        """
        return self._run(index=index)

    def _run(
        self, index: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Categorize a news article using an LLM.

        Args:
            index: Article index (1-based)
            run_manager: Callback manager for the tool run

        Returns:
            Article category
        """
        try:
            # Convert index to integer
            idx = int(index) - 1

            # Get the stored articles
            articles = self.get_stored_articles()

            # Check if we have articles and if the index is valid
            if not articles:
                return "No articles available. Please fetch headlines or search for news first."

            if idx < 0 or idx >= len(articles):
                return f"Invalid article index. Please choose between 1 and {len(articles)}."

            article = articles[idx]

            # Extract relevant information from the article
            title = article.get("title", "")
            description = article.get("description", "")

            # Combine the information for the LLM
            article_text = f"Title: {title}\n\nDescription: {description}"

            # Create a prompt for the LLM
            prompt = f"""
            Categorize the following news article into exactly one of these categories:
            {', '.join(config.VALID_CATEGORIES)}
            
            ARTICLE:
            {article_text}
            
            INSTRUCTIONS:
            1. Return ONLY the category name, with no additional text, explanation, or reasoning
            2. The category must be one of the exact options listed above
            3. Do not include any spaces before or after the category name
            
            CATEGORY:
            """

            # Apply rate limiting for LLM API
            wait_time = _rate_limiter.wait_for_token()
            if wait_time > 0:
                print_tool_action(
                    f"Rate limiting applied for LLM request - waited {wait_time:.2f} seconds"
                )

            # Call the Ollama API
            ollama_response = ollama_client.generate(prompt, temperature=0.3)
            category = ollama_response["response"].strip().lower()

            # Add reasoning to the log for debugging
            logger.info(f"LLM categorized article as: {category} for article: {title}")

            # Validate that the response is a valid category
            if category not in config.VALID_CATEGORIES:
                # Check if the category is in the list after removing any extra whitespace
                clean_category = category.strip()
                if clean_category in config.VALID_CATEGORIES:
                    logger.info(
                        f"Fixed category with whitespace: '{category}' -> '{clean_category}'"
                    )
                    category = clean_category
                else:
                    # Log the reasoning if provided
                    if "reasoning" in ollama_response:
                        logger.warning(
                            f"LLM returned invalid category: {category} with reasoning: {ollama_response['reasoning']}. Defaulting to 'general'."
                        )
                    else:
                        logger.warning(
                            f"LLM returned invalid category: {category}. Defaulting to 'general'."
                        )
                    category = "general"

            return f"Title: {article['title']}\nCategory: {category}"

        except ValueError:
            return "Please provide a valid article number."
        except ToolException as e:
            return str(e)
        except Exception as e:
            logger.error(f"Error categorizing article: {e}")
            return f"Error categorizing article: {str(e)}"
