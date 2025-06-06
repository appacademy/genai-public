"""
Main entry point for the NewsAgent application.
Provides options to run the demo or use the interactive news assistant.
"""

import logging
import time
import sys
from typing import List, Dict, Any

# Import our components
from langchain_tools import (
    GetHeadlinesTool,
    SearchNewsTool,
    SummarizeArticleTool,
    CategorizeArticleTool,
)
from langchain_chains import ArticleInput, multi_processing_chain
from interactive_news import interactive_cli

# Import utility functions for enhanced terminal output
from langchain_utils import (
    print_tool_action,
    print_chain_action,
    print_middleware_action,
    print_error,
    print_success,
    print_info,
    print_header,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_langchain_demo():
    """
    Run a demonstration of the LangChain-based NewsAgent capabilities.
    Shows the power of LangChain tools, chains, and middleware.
    """
    try:
        print_header("LangChain NewsAgent Demo")
        print_info("This demo showcases how LangChain orchestrates news operations")

        # Initialize the tools
        print_tool_action("Initializing LangChain tools...")
        headlines_tool = GetHeadlinesTool()
        search_tool = SearchNewsTool()
        summarize_tool = SummarizeArticleTool()
        categorize_tool = CategorizeArticleTool()

        # Get top headlines
        print_tool_action("Fetching technology headlines using GetHeadlinesTool...")
        headlines_result = headlines_tool.get_headlines(category="technology")
        print_header("Top Technology Headlines")
        print_info(headlines_result)

        # Search for specific news
        print_tool_action(
            "Searching for 'artificial intelligence' news using SearchNewsTool..."
        )
        search_result = search_tool.search_news(query="artificial intelligence")
        print_header("Search Results for 'Artificial Intelligence'")
        print_info(search_result)

        # Get the stored articles for processing
        articles = GetHeadlinesTool.get_stored_articles()
        if articles:
            # Process the first article with the multi-processing chain
            print_chain_action("Preparing to process article with LangChain chains...")
            article = articles[0]

            # Create input for the chain
            print_chain_action("Creating structured input for processing chains...")
            article_input = ArticleInput(
                title=article.get("title", ""),
                description=article.get("description", ""),
                content=article.get("content", ""),
                source=article.get("source", {}).get("name", ""),
                published_at=article.get("publishedAt", ""),
            )

            # Process the article
            print_header("Article Processing with LangChain Chains")
            print_chain_action(
                "Sending article to multi-processing chain (summarization + categorization)..."
            )
            start_time = time.time()
            result = multi_processing_chain.invoke(article_input)
            elapsed = time.time() - start_time

            # Display results
            print_success("Processing complete!")
            print_info(f"Title: {result['title']}")
            print_info(f"Summary: {result['summary']}")
            print_info(
                f"Category: {result['category']} (confidence: {result['confidence']:.2f})"
            )
            print_info(f"Processing completed in {elapsed:.2f} seconds")

        # Demonstrate caching
        print_header("Testing Cache (should be faster)")
        print_middleware_action(
            "Requesting same technology headlines to demonstrate caching..."
        )
        start_time = time.time()
        cached_result = headlines_tool.get_headlines(category="technology")
        elapsed = time.time() - start_time
        print_middleware_action(
            f"Retrieved headlines from cache in {elapsed:.2f} seconds"
        )

        # Test error handling
        print_header("Testing Error Handling")
        print_middleware_action("Testing resilience with invalid category...")
        try:
            # Attempt with invalid category to trigger error handling
            invalid_result = headlines_tool.get_headlines(category="invalid_category")
            print_info(invalid_result)  # This should show an error message
        except Exception as e:
            print_error(f"Handled error as expected: {e}")

        print_success("Demo Completed Successfully!")

    except Exception as e:
        logger.error(f"Error in LangChain demo: {e}")
        print_error(f"Error: {e}")


def display_main_menu():
    """Display the main application menu."""
    print_header("NewsAgent Application (LangChain Edition)")
    print_info("1. Run LangChain Demo")
    print_info("2. Launch Interactive News Assistant")
    print_info("3. Exit")


def main():
    """Main function that displays the menu and handles user input."""
    try:
        while True:
            display_main_menu()
            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                print_info("\nRunning LangChain Demo...\n")
                run_langchain_demo()
                input("\nPress Enter to return to the main menu...")

            elif choice == "2":
                print_info("\nLaunching Interactive News Assistant...\n")
                interactive_cli()  # Call the interactive CLI function

            elif choice == "3":
                print_success("\nExiting NewsAgent Application. Goodbye!")
                break

            else:
                print_error("\nInvalid choice. Please enter a number between 1 and 3.")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting.")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
