"""
Interactive CLI for the NewsAgent application.
Allows users to fetch headlines, search for news, and process articles using AI.

This implementation uses LangChain tools and chains for all operations.
"""

import logging
import time
from typing import List, Dict, Any, Optional
import config

# Import LangChain components
from langchain_tools import (
    GetHeadlinesTool,
    SearchNewsTool,
    SummarizeArticleTool,
    CategorizeArticleTool,
)
from langchain_chains import (
    ArticleInput,
    summarization_chain,
    categorization_chain,
    multi_processing_chain,
)

# Import utility functions for enhanced terminal output
from langchain_utils import (
    print_tool_action,
    print_chain_action,
    print_middleware_action,
    print_error,
    print_success,
    print_info,
    print_header,
    time_it,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def display_main_menu() -> None:
    """Display the main menu options."""
    print_header("News Assistant (LangChain Edition)")
    print_info("1. Get top headlines by category")
    print_info("2. Search for news")
    print_info("3. Exit")


def display_article_menu() -> None:
    """Display the article operations menu."""
    print_header("Options")
    print_info("1. Show more articles")
    print_info("2. Analyze article (summary + category)")
    print_info("3. Analyze multiple articles (up to 3)")
    print_info("4. Return to main menu")


def display_articles(
    articles: List[Dict[str, Any]], start_idx: int = 0, count: int = 10
) -> None:
    """
    Display a formatted list of articles.

    Args:
        articles: List of article dictionaries
        start_idx: Starting index for display
        count: Number of articles to display
    """
    if not articles:
        print_info("No articles found.")
        return

    end_idx = min(start_idx + count, len(articles))

    print_header(f"Articles ({start_idx+1}-{end_idx} of {len(articles)})")
    for i, article in enumerate(articles[start_idx:end_idx], start_idx + 1):
        print_info(f"{i}. {article['title']}")
        print_info(f"   Source: {article.get('source', {}).get('name', 'Unknown')}")
        print_info(f"   Published: {article.get('publishedAt', 'Unknown')}")
        print_info("")


# Create a mapping of 3-letter abbreviations to full category names
CATEGORY_ABBREV = {cat[:3]: cat for cat in config.VALID_CATEGORIES}


@time_it
def get_headlines() -> List[Dict[str, Any]]:
    """
    Interactive function to get headlines by category using LangChain tools.

    Returns:
        List of retrieved articles
    """
    # Initialize the tool
    print_tool_action("Initializing GetHeadlinesTool...")
    headlines_tool = GetHeadlinesTool()

    # Format categories with abbreviations
    categories_display = ", ".join(
        [f"{cat} ({cat[:3]})" for cat in config.VALID_CATEGORIES]
    )
    print_info(f"\nAvailable categories: {categories_display}")
    category = (
        input("Enter category name or abbreviation (or press Enter for all): ")
        .strip()
        .lower()
    )

    # Check if input is an abbreviation and convert if needed
    if category in CATEGORY_ABBREV:
        category = CATEGORY_ABBREV[category]
        print_info(f"Using full category name: {category}")

    # Validate category if provided
    if category and category not in config.VALID_CATEGORIES and category != "":
        print_error(f"Invalid category. Please choose from: {categories_display}")
        return []

    try:
        # Convert empty input to "all" for the tool
        cat = "all" if category == "" else category
        print_tool_action(f"Fetching {'all' if cat == 'all' else cat} headlines...")

        # Get headlines using the LangChain tool
        result = headlines_tool.get_headlines(category=cat)

        # Get the stored articles
        articles = headlines_tool.get_stored_articles()
        print_success(f"Retrieved {len(articles)} articles")

        if articles:
            display_articles(articles)
            handle_article_operations(articles)

        return articles

    except Exception as e:
        logger.error(f"Error fetching headlines: {e}")
        print_error(f"Error: {e}")
        return []


@time_it
def search_news() -> List[Dict[str, Any]]:
    """
    Interactive function to search for news using LangChain tools.

    Returns:
        List of retrieved articles
    """
    # Initialize the tool
    print_tool_action("Initializing SearchNewsTool...")
    search_tool = SearchNewsTool()

    query = input("\nEnter search term: ").strip()
    if not query:
        print_error("Search term cannot be empty.")
        return []

    try:
        print_tool_action(f"Searching for '{query}'...")

        # Search for news using the LangChain tool
        result = search_tool.search_news(query=query)

        # Get the stored articles
        articles = search_tool.get_stored_articles()
        print_success(f"Retrieved {len(articles)} articles")

        if articles:
            display_articles(articles)
            handle_article_operations(articles)

        return articles

    except Exception as e:
        logger.error(f"Error searching news: {e}")
        print_error(f"Error: {e}")
        return []


@time_it
def analyze_article(article: Dict[str, Any]) -> None:
    """
    Process both summary and category for a single article using LangChain chains.

    Args:
        article: Article to analyze
    """
    print_chain_action(f"Analyzing: {article['title']}...")

    # Create input for the chain
    print_chain_action("Creating structured input for processing chains...")
    article_input = ArticleInput(
        title=article.get("title", ""),
        description=article.get("description", ""),
        content=article.get("content", ""),
        source=article.get("source", {}).get("name", ""),
        published_at=article.get("publishedAt", ""),
    )

    # Process the article with the multi-processing chain
    print_chain_action("Sending article to multi-processing chain...")
    result = multi_processing_chain.invoke(article_input)

    # Display combined results
    print_header("Article Analysis")
    print_info(f"Title: {result['title']}")
    print_info(f"Summary: {result['summary']}")
    print_info(
        f"Category: {result['category']} (confidence: {result['confidence']:.2f})"
    )
    print_success("Analysis complete!")


def select_multiple_articles(
    articles: List[Dict[str, Any]], visible_end: int
) -> List[int]:
    """
    Allow selection of up to 3 articles for analysis.

    Args:
        articles: List of articles
        visible_end: Maximum article index that can be selected

    Returns:
        List of selected article indices (0-based)
    """
    print_info("\nSelect up to 3 articles for analysis.")
    print_info("Enter article numbers separated by commas (e.g., '1,3,5'):")

    while True:
        selection = input(f"Article numbers (1-{visible_end}): ").strip()
        try:
            # Parse article indices
            indices = [int(idx.strip()) for idx in selection.split(",")]

            # Validate selection
            if len(indices) > 3:
                print_error("You can select at most 3 articles.")
                continue

            if len(indices) != len(set(indices)):
                print_error("Please select each article only once.")
                continue

            if any(idx < 1 or idx > visible_end for idx in indices):
                print_error(f"Article numbers must be between 1 and {visible_end}.")
                continue

            # Convert to 0-based indices for internal use
            return [idx - 1 for idx in indices]

        except ValueError:
            print_error("Please enter valid article numbers separated by commas.")


def handle_article_operations(articles: List[Dict[str, Any]]) -> None:
    """
    Handle operations on articles (show more, analyze, etc.).

    Args:
        articles: List of articles
    """
    current_idx = 10

    while True:
        display_article_menu()
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":  # Show more articles
            if current_idx >= len(articles):
                print_info("No more articles to display.")
            else:
                display_articles(articles, current_idx, 10)
                current_idx += 10

        elif choice == "2":  # Analyze single article
            try:
                # Calculate the visible range
                visible_end = min(current_idx, len(articles))
                article_idx = int(
                    input(f"\nEnter article number to analyze (1-{visible_end}): ")
                )
                if article_idx < 1 or article_idx > visible_end:
                    print_error(
                        f"Invalid article number. Please choose between 1 and {visible_end}."
                    )
                    continue

                article = articles[article_idx - 1]
                analyze_article(article)

            except ValueError:
                print_error("Please enter a valid number.")
            except Exception as e:
                logger.error(f"Error analyzing article: {e}")
                print_error(f"Error: {e}")

        elif choice == "3":  # Analyze multiple articles
            try:
                # Calculate the visible range
                visible_end = min(current_idx, len(articles))

                # Get article selections
                selected_indices = select_multiple_articles(articles, visible_end)

                print_chain_action(f"Processing {len(selected_indices)} articles...")

                # Process each selected article
                for i, idx in enumerate(selected_indices):
                    article = articles[idx]
                    print_info(f"\nArticle {i+1} of {len(selected_indices)}:")
                    analyze_article(article)
                    if i < len(selected_indices) - 1:
                        print_info("\n" + "-" * 50)  # Separator between articles

                print_success("All selected articles processed successfully!")

            except Exception as e:
                logger.error(f"Error analyzing multiple articles: {e}")
                print_error(f"Error: {e}")

        elif choice == "4":  # Return to main menu
            break

        else:
            print_error("\nInvalid choice. Please enter a number between 1 and 4.")


def interactive_cli():
    """Main interactive CLI function."""
    print_header("News Assistant (LangChain Edition)")
    print_info("Initializing LangChain components...")
    try:
        print_success("LangChain tools initialized successfully.")
        print_info(
            "This assistant demonstrates how LangChain orchestrates news operations"
        )

        articles = []  # Store the most recent articles

        while True:
            display_main_menu()
            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                articles = get_headlines()

            elif choice == "2":
                articles = search_news()

            elif choice == "3":
                print_success("\nExiting News Assistant. Goodbye!")
                break

            else:
                print_error("\nInvalid choice. Please enter a number between 1 and 3.")

    except Exception as e:
        logger.error(f"Error in interactive CLI: {e}")
        print_error(f"\nAn error occurred: {e}")
        print_info("Exiting News Assistant.")


if __name__ == "__main__":
    interactive_cli()
