# NewsAgent Application (LangChain Edition)

A robust news retrieval and processing system that integrates with the News API and uses Ollama for AI-powered content processing. This refactored version uses LangChain as the central orchestration layer, with tools, chains, and middleware for resilient API operations.

## Setup

1. Copy the file `.env.template` into the same directory. 
2. Name the new file `.env`.
3. If desired, replace the OLLAMA_API_URL key with your own URL.

```bash
cp .env.template .env
```

### Requirements

- Python 3.12
- Ollama with the Gemma 3:4b model installed
  - Run `ollama pull gemma3:4b` to download the model
- News API key (obtain from [newsapi.org](https://newsapi.org/))

## Usage

Run the application using:

```bash
python app.py
```

This will present you with a menu to choose between:

1. **LangChain Demo** - Demonstrates the LangChain-based NewsAgent capabilities
2. **Interactive News Assistant** - Allows you to interactively search for news, get headlines, and process articles
3. **Exit** - Exit the application

## Features

- Fetch top headlines by category
- Search for news articles
- Generate article summaries using AI
- Categorize articles using AI
- Resilient API integration with caching and rate limiting
- Conversational agent interface powered by LangChain
- Memory-powered interactions that maintain conversation context
- Agent-based reasoning for complex news queries

## Project Architecture

The application has a modular architecture organized by functionality:

### Core Components

- **app.py** - Main entry point with menu system and demo
- **config.py** - Configuration settings and constants
- **cache.py** - In-memory caching with time-based expiration
- **rate_limiter.py** - Token bucket algorithm to prevent API quota exhaustion
- **error_handler.py** - Retry logic with exponential backoff
- **ollama_client.py** - Interface to the Ollama API for LLM capabilities

### LangChain Components

- **langchain_tools.py** - LangChain tools for news operations
- **langchain_chains.py** - Processing chains for LLM operations
- **langchain_middleware.py** - Middleware for resilience features
- **langchain_agent.py** - ReAct agent for conversational interactions
- **langchain_utils.py** - Utility functions for LangChain components

### UI Components

- **interactive_news.py** - CLI interface for news operations

## LangChain Integration

The application has been refactored to use LangChain as the central orchestration layer:

### LangChain Tools

The application provides the following LangChain tools:

- **GetHeadlinesTool**: Fetch top headlines by category
- **SearchNewsTool**: Search for news articles by query
- **SummarizeArticleTool**: Generate a concise summary of a specific article
- **CategorizeArticleTool**: Determine the category of a specific article

### LangChain Chains

The application uses the following LangChain chains:

- **Summarization Chain**: Chain for generating article summaries
- **Categorization Chain**: Chain for categorizing articles
- **Multi-Processing Chain**: Combined chain for both summarization and categorization

### LangChain Middleware

The application implements middleware for resilience:

- **CachingMiddleware**: Adds caching to LangChain runnables
- **RateLimitingMiddleware**: Adds rate limiting to LangChain runnables
- **RetryMiddleware**: Adds retry logic to LangChain runnables

### Using the LangChain Agent

The LangChain agent is available for programmatic use in your Python code:

```python
from langchain_agent import NewsAgentLangChain

# Initialize the agent
agent = NewsAgentLangChain()

# Run a query
response = agent.run("What are the latest technology headlines?")
print(response)

# Ask a follow-up question (agent maintains conversation context)
response = agent.run("Summarize the first article")
print(response)
```
