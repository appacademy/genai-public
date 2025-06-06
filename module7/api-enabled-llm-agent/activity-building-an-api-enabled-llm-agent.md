# Building an API-Enabled LLM Agent with NewsAgent



## Overview

In this hands-on activity, you'll build a `NewsAgent` class that integrates with a news API, implementing professional-grade error handling, rate limiting, and caching. This system will efficiently fetch and process news articles while being resilient to common API integration challenges. The activity mirrors real-world LLM agent development scenarios where you need to connect language models with external data sources while optimizing for reliability and performance.



## Learning Objectives

By completing this activity, you will:
1. Implement secure API authentication patterns that protect credentials while providing reliable access to external news data
2. Develop a resilient error handling system with retry logic and circuit breakers to maintain functionality during API disruptions
3. Create an effective caching layer that reduces unnecessary API calls while maintaining data freshness
4. Build rate limiting mechanisms using techniques like exponential backoff to prevent quota exhaustion
5. Design a modular agent architecture that separates concerns between API interaction, data processing, and LLM integration



## Time Estimate

120 minutes



## Prerequisites

- Python 3.12
- Basic understanding of API integration and error handling
- Familiarity with Python libraries and package installation
- Ollama installed locally with the gemma3:4b model
- News API key (free tier available)



## Setup Instructions

### Step 1: Clone the Repository

Clone the starter code repository to your local machine:

```bash
git clone https://github.com/[organization]/news-agent-starter.git
cd news-agent-starter
```



### Step 2: Create and Activate a Virtual Environment

Create and then activate a virtual environment for your project using the commands for your system:

- **Mac/Linux**:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **Windows (PowerShell)**:

  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  ```

- **Windows (Git Bash)**:

  ```bash
  python -m venv .venv
  source .venv/Scripts/activate
  ```

After activation, your terminal prompt should change (e.g., `(venv)` appears).



### Step 3: Install Dependencies

With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

The requirements.txt file contains the following dependencies:

```
requests==2.32.3
python-dotenv==1.0.1
numpy<2.0.0,>=1.0.0
langchain
langchain-community
langchain-core>=0.1.33
```



### Step 4: Configure Environment

1. Create a `.env` file from the template:

   ```bash
   # Mac/Linux
   cp .env.template .env
   
   # Windows (PowerShell/Command Prompt)
   copy .env.template .env
   ```

2. Obtain a free News API key from [newsapi.org](https://newsapi.org/) and add it to your `.env` file.

3. The default configuration uses Ollama at `http://localhost:11434`. If you're using a different URL, update the `.env` file.



### Step 5: Start Ollama

1. Ensure Ollama is installed on your system. If not, download it from [ollama.ai](https://ollama.ai).

2. Start Ollama with the gemma3:4b model:

   ```bash
   # All operating systems
   ollama run gemma3:4b
   ```

   This will download the model if it's not already on your system and start the Ollama service.



## Key Concepts

### API Integration and Authentication

The NewsAgent application demonstrates secure API integration with:

1. **Credential Management**: Using environment variables to securely store API keys
2. **Request Authentication**: Properly authenticating API requests
3. **Parameter Validation**: Validating input parameters before making API calls
4. **Response Processing**: Handling API responses and extracting relevant data

### Resilience Mechanisms

The application implements several resilience patterns:

1. **Retry Logic**: Automatically retrying failed API calls with exponential backoff
2. **Circuit Breakers**: Preventing calls to failing services to avoid cascading failures
3. **Error Handling**: Specialized handling for different HTTP error codes
4. **Graceful Degradation**: Providing fallback behavior when services are unavailable

### Caching and Rate Limiting

Efficient API usage is achieved through:

1. **In-Memory Cache**: Storing API responses to reduce duplicate requests
2. **Time-Based Expiration**: Ensuring data freshness with TTL (Time To Live)
3. **Token Bucket Algorithm**: Implementing rate limiting to prevent quota exhaustion
4. **Request Batching**: Optimizing API usage by batching requests when possible

### LLM Integration

The application demonstrates LLM integration for content processing:

1. **Article Summarization**: Using LLMs to generate concise summaries
2. **Content Categorization**: Classifying articles into predefined categories
3. **Prompt Engineering**: Creating effective prompts for specific tasks
4. **Response Validation**: Handling the unpredictability of LLM outputs



## LangChain Framework

This activity uses the LangChain framework to orchestrate interactions between LLMs, APIs, and other components. LangChain provides a structured approach to building LLM-powered applications with modular, reusable components.

> **Note**: For a comprehensive introduction to LangChain and how it's implemented in this activity, refer to the [LangChain Reference Guide](resources/langchain_reference_guide.md). This guide explains key concepts like Tools, Chains, Agents, and Middleware, along with diagrams showing how these components interact in the NewsAgent application.



## Activity Tasks

In this activity, you'll implement several key components of the NewsAgent system by completing the TODO items in the starter code. Each task focuses on an important aspect of LangChain integration with external API systems.

### Task 1: Implement LangChain Tool for Headlines Fetching

Your first task is to implement the tool for fetching headlines in the `langchain_tools.py` file. 

1. Complete the `_run` method in the `GetHeadlinesTool` class. This method handles fetching news headlines with category filtering. 

    **Step 1.1**. Find the TODO comment: "Implement a LangChain tool for fetching headlines" and follow the steps below.
    
    **Step 1.2**. Find the TODO comment: "Validate the provided category against valid categories" and add this code snippet:
    
    ```python
    try:
        # Convert 'all' to None for the API
        cat = None if category.lower() == "all" else category.lower()

        # Validate category if provided
        if cat and cat not in config.VALID_CATEGORIES:
            return f"Invalid category: {category}. Valid categories are: {', '.join(config.VALID_CATEGORIES)}"
    ```
    
    This code converts the "all" category to None for the API and validates that any specific category provided is in the list of valid categories defined in the configuration.
    
    **Step 1.3**. Find the TODO comment: "Prepare API parameters (use 'all' or a specific category)" and add this code snippet:
    
    ```python
        # Set up parameters
        endpoint = f"{NEWS_API_BASE_URL}/top-headlines"
        params = {"country": config.DEFAULT_COUNTRY}

        if cat:
            params["category"] = cat
    ```
    
    This code sets up the API endpoint and parameters, including the default country from the configuration. It adds the category parameter only if a specific category was provided.
    
    **Step 1.4**. Find the TODO comment: "Call the API using _make_api_request with proper error handling" and add this code snippet:
    
    ```python
        # Make the API request
        result = self._make_api_request(endpoint, params)
        articles = result["articles"]
    ```
    
    This code makes the API request using the prepared endpoint and parameters, then extracts the articles from the response.
    
    **Step 1.5**. Find the TODO comment: "Store the retrieved articles for use by other tools" and add this code snippet:
    
    ```python
        # Store articles for later use
        self._store_articles(articles)
    ```
    
    This code stores the retrieved articles for later use by other tools in the application.
    
    **Step 1.6**. Find the TODO comment: "Format the articles into a readable string response and return it" and add this code snippet:
    
    ```python
        # Format the results
        return self._format_articles(articles)

    except ToolException as e:
        return str(e)
    except Exception as e:
        logger.error(f"Error getting headlines: {e}")
        return f"Error fetching headlines: {str(e)}"
    ```
    
    This code formats the articles into a readable string and returns it. It also includes error handling for both specific tool exceptions and general exceptions, logging errors and returning appropriate error messages.


2. Implement the `_format_articles` method to display news headlines in a readable format.

    **Step 1.1*7. Find the TODO comment: "Task 2 - Format Articles for Display" and follow the steps below.
    
    **Step 1.8**. Find the TODO comment: "Handle empty results" and add this code snippet:
    
    ```python
    if not articles:
        return "No articles found."
    
    result = f"Found {len(articles)} articles:\n\n"
    ```
    
    This code checks if the articles list is empty and returns an appropriate message. If articles exist, it initializes the result string with a count of found articles.
    
    **Step 1.9**. Find the TODO comment: "Format and display up to 5 articles" and add this code snippet:
    
    ```python
    # Display up to 5 articles
    for i, article in enumerate(articles[:5], 1):
        result += f"{i}. {article['title']}\n"
        result += f"   Source: {article.get('source', {}).get('name', 'Unknown')}\n"
        result += f"   Published: {article.get('publishedAt', 'Unknown')}\n\n"
    ```
    
    This code loops through up to 5 articles, formatting each with a numbered title, source name, and publication date. The `.get()` method is used to safely access nested dictionary values with fallback defaults.
    
    **Step 1.10**. Find the TODO comment: "Add summary if there are more articles" and add this code snippet:
    
    ```python
    if len(articles) > 5:
        result += f"... and {len(articles) - 5} more articles.\n"
    
    return result
    ```
    
    This code adds a summary line if there are more than 5 articles, indicating how many additional articles were found but not displayed. Finally, it returns the formatted result string.


### Task 2: Implement LangChain Tool for Article Summarization

1. Implement LangChain Tool for Article Summarization in the `langchain_tools.py` file.

    **Step 2.1**. Find the TODO comment: "Implement a LangChain tool for article summarization" and follow the steps below.
    
    **Step 2.2**. Find the TODO comment: "1. Convert and validate the article index" and add this code snippet:
    
    ```python
    try:
        # Convert index to integer
        idx = int(index) - 1
    ```
    
    This code converts the user-provided index string to an integer and adjusts it to be zero-based for array indexing.
    
    **Step 2.3**. Find the TODO comment: "2. Retrieve the article from stored articles" and add this code snippet:
    
    ```python
        # Get the stored articles
        articles = self.get_stored_articles()

        # Check if we have articles and if the index is valid
        if not articles:
            return "No articles available. Please fetch headlines or search for news first."

        if idx < 0 or idx >= len(articles):
            return f"Invalid article index. Please choose between 1 and {len(articles)}."

        article = articles[idx]
    ```
    
    This code retrieves the stored articles, checks if any articles exist, validates that the index is within the valid range, and then gets the selected article.
    
    **Step 2.4**. Find the TODO comment: "3. Extract title, description, and content from the article" and add this code snippet:
    
    ```python
        # Extract relevant information from the article
        title = article.get("title", "")
        description = article.get("description", "")
        content = article.get("content", "")

        # Combine the information for the LLM
        article_text = (
            f"Title: {title}\n\nDescription: {description}\n\nContent: {content}"
        )
    ```
    
    This code extracts the title, description, and content from the article and combines them into a formatted text for the LLM to process.
    
    **Step 2.5**. Find the TODO comment: "4. Create an effective prompt for the LLM summarization task" and add this code snippet:
    
    ```python
        # Create a prompt for the LLM
        prompt = f"""
        Below is a news article. Please provide a concise summary in 3-4 sentences.
        Focus on the main points and key information.
        
        ARTICLE:
        {article_text}
        
        SUMMARY:
        """
    ```
    
    This code creates a clear prompt for the LLM, instructing it to generate a concise 3-4 sentence summary focusing on the main points of the article.
    
    **Step 2.6**. Find the TODO comment: "5. Apply rate limiting before calling the LLM" and add this code snippet:
    
    ```python
        # Apply rate limiting for LLM API
        wait_time = _rate_limiter.wait_for_token()
        if wait_time > 0:
            print_tool_action(
                f"Rate limiting applied for LLM request - waited {wait_time:.2f} seconds"
            )
    ```
    
    This code applies rate limiting to prevent API quota exhaustion, waiting for a token if necessary and reporting the wait time.
    
    **Step 2.7**. Find the TODO comment: "6. Call the Ollama API to generate the summary" and add this code snippet:
    
    ```python
        # Call the Ollama API
        ollama_response = ollama_client.generate(prompt)
        summary = ollama_response["response"].strip()
    ```
    
    This code calls the Ollama API with the prepared prompt and extracts the summary from the response.
    
    **Step 2.8**. Find the TODO comment: "7. Return the formatted result" and add this code snippet:
    
    ```python
        return f"Title: {title}\nSummary: {summary}"
    ```
    
    This code formats the final output with the article title and the generated summary.
    
    **Step 2.9**. Find the TODO comment: "8. Properly handle all exception cases" and add this code snippet:
    
    ```python
    except ValueError:
        return "Please provide a valid article number."
    except ToolException as e:
        return str(e)
    except Exception as e:
        logger.error(f"Error summarizing article: {e}")
        return f"Error summarizing article: {str(e)}"
    ```
    
    This code handles various exception cases, including value errors when the index isn't a valid number, tool-specific exceptions, and any other unexpected errors.


### Task 3: Implement LangChain Chains for Content Processing

1. This task involves implementing specialized LangChain chains in the `langchain_chains.py` file to process article content.  We'll need to work on three key functions. First, we'll implement the `create_summarization_chain` function.

    **Step 3.1**. Find the TODO comment: "Implement a LangChain chain for article summarization" and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "Create an LLM with appropriate temperature for factual summarization" and add this code snippet:
    
    ```python
    # Create the LLM
    llm = create_llm(temperature=0.5)  # Lower temperature for more factual summaries
    ```
    
    This code creates a language model with a temperature of 0.5, which is appropriate for generating factual summaries rather than creative content.
    
    **Step 3.3**. Find the TODO comment: "Design a prompt template for article summarization" and add this code snippet:
    
    ```python
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
    ```
    
    This code creates a prompt template that instructs the model to provide a concise 3-4 sentence summary of the article, focusing on main points and key information.
    
    **Step 3.4**. Find the TODO comment: "Create the chain by composing: prompt | llm | StrOutputParser()" and add this code snippet:
    
    ```python
    # Create the chain
    chain = prompt | llm | StrOutputParser()
    ```
    
    This code composes a chain using the pipe syntax, connecting the prompt template to the language model and then to a string output parser.
    
    **Step 3.5**. Find the TODO comment: "Add preprocessing logic to handle different input formats" and add this code snippet:
    
    ```python
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
    ```
    
    This code defines a preprocessing function that handles different input formats, whether they are ArticleInput objects or dictionaries, and converts them to a consistent format.
    
    **Step 3.6**. Find the TODO comment: "Return the complete chain with preprocessing" and add this code snippet:
    
    ```python
    # Add preprocessing to the chain
    return RunnableLambda(preprocess_input) | chain
    ```
    
    This code adds the preprocessing function to the chain using RunnableLambda and returns the complete chain that can now handle different input formats.


2. Next, implement the `create_summarization_chain` function in the `langchain_chains.py` file with a similar structure but designed for categorization rather than summarization.

    **Step 3.7**. Find the TODO comment: "Implement a LangChain chain for article categorization" and follow the steps below.
    
    **Step 3.8**. Find the TODO comment: "Create an LLM with appropriate temperature for consistent categorization" and add this code snippet:
    
    ```python
    # Create the LLM
    llm = create_llm(
        temperature=0.3
    )  # Lower temperature for more consistent categorization
    ```
    
    This code creates an LLM instance with a low temperature setting (0.3) to ensure more consistent and predictable categorization results.
    
    **Step 3.9**. Find the TODO comment: "Design a prompt template with clear instructions for categorization" and add this code snippet:
    
    ```python
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
    ```
    
    This code creates a prompt template that provides clear instructions for categorizing news articles, including the list of valid categories and formatting requirements.
    
    **Step 3.10**. Find the TODO comment: "Create the base chain: prompt | llm | StrOutputParser()" and add this code snippet:
    
    ```python
    # Create the chain
    chain = prompt | llm | StrOutputParser()
    ```
    
    This code creates the basic chain using the pipe syntax, connecting the prompt template to the LLM and then to a string output parser.
    
    **Step 3.11**. Find the TODO comment: "Add preprocessing to format the input for the prompt" and add this code snippet:
    
    ```python
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
    ```
    
    This code defines a preprocessing function that handles different input formats (either dictionaries or ArticleInput objects) and formats them for the prompt template.
    
    **Step 3.12**. Find the TODO comment: "Add post-processing to validate that categories match allowed values" and add this code snippet:
    
    ```python
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
    ```
    
    This code defines a post-processing function that validates the category returned by the LLM, ensuring it's one of the valid categories defined in the configuration.
    
    **Step 3.13**. Find the TODO comment: "Combine the preprocessing, chain, and post-processing" and add this code snippet:
    
    ```python
    # Combine preprocessing, chain, and validation
    return (
        RunnableLambda(preprocess_and_validate)
        | chain
        | RunnableLambda(validate_category)
    )
    ```
    
    This code combines the preprocessing function, the base chain, and the validation function into a complete pipeline using the pipe syntax, and returns the final chain.


3. Lastly, implement the `create_multi_processing_chain` function that combines both summarization and categorization. We'll create a processing function that runs the previously created chains on the same input and combines their results into a unified output structure. Then, we'll wrap this function in a RunnableLambda to create the final chain. This task demonstrates how to build complex chain compositions for handling sophisticated content processing operation

    **Step 3.14**. Find the TODO comment: "Implement a LangChain chain that combines multiple operations" and follow the steps below.
    
    **Step 3.15**. Find the TODO comment: "Reuse the previously created chains" and add this code snippet:
    
    ```python
    # Create the individual chains
    summarization_chain = create_summarization_chain()
    categorization_chain = create_categorization_chain()
    ```
    
    This code creates instances of the summarization and categorization chains that you implemented in previous steps.
    
    **Step 3.16**. Find the TODO comment: "Create a processing function" and add this code snippet:
    
    ```python
    # Define the combined chain
    def process_article(data: Union[Dict[str, Any], ArticleInput]) -> Dict[str, Any]:
        """Process an article with both summarization and categorization."""
        # Run summarization
        summary = summarization_chain.invoke(data)

        # Run categorization
        category_result = categorization_chain.invoke(data)
    ```
    
    This code defines a function that takes article data as input and processes it through both the summarization and categorization chains.
    
    **Step 3.17**. Find the TODO comment: "Combine the results" and add this code snippet:
    
    ```python
        # Combine results
        return {
            "title": (
                data.title if isinstance(data, ArticleInput) else data.get("title", "")
            ),
            "summary": summary,
            "category": category_result["category"],
            "confidence": category_result.get("confidence", 1.0),
        }
    ```
    
    This code combines the results from both chains into a single dictionary containing the article title, summary, category, and confidence score.
    
    **Step 3.18**. Find the TODO comment: "Return the combined chain" and add this code snippet:
    
    ```python
    return RunnableLambda(process_article)
    ```
    
    This code wraps the processing function in a RunnableLambda to create the final chain that can be invoked with article data.


### Task 4: Implement Middleware for LangChain Resilience

1. For this task, you'll implement middleware components in the `langchain_middleware.py` file to add resilience features to LangChain operations.

    **Step 4.1**. Find the TODO comment: "Implement caching logic for LangChain invocations" and follow the steps below.
    
    **Step 4.2**. Find the TODO comment: "1. Generate a cache key from the input data" and add this code snippet:
    
    ```python
    cache_key = self.cache_key_fn(input_data)
    ```
    
    This code uses the provided cache key function to generate a unique key based on the input data.
    
    **Step 4.3**. Find the TODO comment: "2. Check if a result exists in the cache" and add this code snippet:
    
    ```python
    # Check if we have a cached result
    cached_result = self.cache.get("runnable", {"key": cache_key})
    ```
    
    This code checks if there's already a result in the cache with the generated key.
    
    **Step 4.4**. Find the TODO comment: "3. If cached, return the cached result" and add this code snippet:
    
    ```python
    if cached_result:
        logger.info(f"Returning cached result for {cache_key}")
        return cast(Output, cached_result)
    ```
    
    This code returns the cached result if one exists, avoiding redundant computation.
    
    **Step 4.5**. Find the TODO comment: "4. Otherwise, invoke the runnable to get a fresh result" and add this code snippet:
    
    ```python
    # No cached result, invoke the runnable
    logger.info(f"Cache miss for {cache_key}, invoking runnable")
    result = self.runnable.invoke(input_data, config)
    ```
    
    This code invokes the runnable to compute a fresh result when there's no cached result available.
    
    **Step 4.6**. Find the TODO comment: "5. Cache the fresh result" and add this code snippet:
    
    ```python
    # Cache the result
    self.cache.set("runnable", {"key": cache_key}, result)
    ```
    
    This code stores the newly computed result in the cache for future use.
    
    **Step 4.7**. Find the TODO comment: "6. Return the result" and add this code snippet:
    
    ```python
    return result
    ```
    
    This code returns the fresh result to the caller.


2. Next, implement the `with_resilience` function that composes multiple middleware layers to create a comprehensive resilience strategy. Apply middleware in the correct order: retry as the outermost layer, rate limiting in the middle, and caching as the innermost layer. This order ensures that caching happens before rate limiting is applied, and that retry logic surrounds the entire operation. Configure each middleware with appropriate parameters for resilience including cache expiry times, request rate limits, retry attempts, and backoff factors. Structure the middleware composition carefully to ensure optimal performance and proper error handling throughout the system. This task focuses on implementing industry-standard resilience patterns to make your LangChain operations robust against various failure scenarios.

---

# Rewritten Passage

2. Next, implement the `with_resilience` function that composes multiple middleware layers to create a comprehensive resilience strategy. We'll apply middleware in the correct order: retry as the outermost layer, rate limiting in the middle, and caching as the innermost layer. This order ensures that caching happens before rate limiting is applied, and that retry logic surrounds the entire operation.

    **Step 4.8**. Find the TODO comment: "Implement the middleware composition pattern for resilience" and follow the steps below.
    
    **Step 4.9**. Find the TODO comment: "Apply middleware in order: retry -> rate limiting -> caching" and add this code snippet:
    
    ```python
    # Apply middleware in order: retry -> rate limiting -> caching
    # This order ensures that caching happens before rate limiting,
    # and retries happen for the entire operation
    resilient_runnable = RetryMiddleware(
        RateLimitingMiddleware(
            CachingMiddleware(
                runnable, cache_key_fn=cache_key_fn, expiry_time=cache_expiry
            ),
            requests_per_minute=requests_per_minute,
        ),
        max_retries=max_retries,
        backoff_factor=backoff_factor,
        retry_on=retry_on,
    )
    ```
    
    This code composes three middleware layers in the correct order: retry as the outermost layer, rate limiting in the middle, and caching as the innermost layer. The CachingMiddleware is configured with the provided cache key function and expiry time. The RateLimitingMiddleware is configured with the specified requests per minute. The RetryMiddleware is configured with the maximum number of retries, backoff factor, and exception types to retry on.
    
    **Step 4.10**. Find the TODO comment: "Return the composed, resilient runnable" and add this code snippet:
    
    ```python
    return resilient_runnable
    ```
    
    This code returns the fully composed runnable with all resilience features applied, making it ready to use in your application.


### Task 5: Implement LangChain ReAct Agent

1. In this task, we'll enhance the LangChain agent in the `langchain_agent.py` file by implementing the LangChain ReAct Agent using the `_create_agent` method. This task demonstrates how to build sophisticated agents with reasoning and action capabilities using the LangChain framework, which creates a system that can effectively orchestrate various tools to accomplish complex tasks.

    **Step 5.1**. Find the TODO comment: "Implement the LangChain ReAct agent" and follow the steps below.
    
    **Step 5.2**. Find the TODO comment: "Create a prompt template that includes tools, chat history, and agent_scratchpad" and add this code snippet:
    
    ```python
    # Define the ReAct prompt template with required variables
    template = """You are a helpful news assistant that can fetch headlines, search for news, and analyze articles.

    You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    {chat_history}

    Question: {input}
    {agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)
    ```
    
    This code creates a prompt template that structures how the agent will interact. It includes placeholders for tools information, available tool names, chat history, user input, and a scratchpad for the agent's reasoning process. The template follows the ReAct pattern with clear formatting for Question, Thought, Action, Action Input, Observation, and Final Answer.
    
    **Step 5.3**. Find the TODO comment: "Create the ReAct agent using create_react_agent with the LLM, tools, and prompt" and add this code snippet:
    
    ```python
    # Create the ReAct agent
    agent = create_react_agent(self.llm, self.tools, prompt)
    ```
    
    This code creates a ReAct agent using the LangChain function `create_react_agent()`, passing in the language model, tools, and the prompt template you defined earlier. This sets up the core agent that will perform reasoning and take actions.
    
    **Step 5.4**. Find the TODO comment: "Create the agent executor with appropriate parameters" and add this code snippet:
    
    ```python
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=self.tools,
        memory=self.memory,
        verbose=True,
        handle_parsing_errors=True,
    )
    ```
    
    This code creates an `AgentExecutor` that will run the agent. It configures the executor with the agent you created, the available tools, memory for maintaining conversation context, and enables verbose mode for debugging. The `handle_parsing_errors=True` parameter ensures the agent can gracefully handle cases where it produces malformed outputs.
    
    **Step 5.5**. Find the TODO comment: "Return the configured agent executor" and add this code snippet:
    
    ```python
    return agent_executor
    ```
    
    This code returns the fully configured agent executor that's ready to process user queries and perform actions using the available tools.


### Task 6: Implement User Query Processing

1. Implement the `run` method in the `langchain.py` file to process user queries. This task focuses on creating a smooth user experience with LangChain agents, ensuring that users can easily interact with the powerful capabilities you've built throughout the previous tasks.

    **Step 6.1**. Find the TODO comment: "Task 6 - Implement User Query Processing" and follow the steps below.
    
    **Step 6.2**. Find the TODO comment: "Log the user query" and add this code snippet:
    
    ```python
    try:
        logger.info(f"Processing user query: {query}")
    ```
    
    This code logs the user's query for debugging purposes, providing visibility into what users are asking.
    
    **Step 6.3**. Find the TODO comment: "Invoke the LangChain agent with the query" and add this code snippet:
    
    ```python
        response = self.agent.invoke({"input": query})
    ```
    
    This code invokes the LangChain agent with the user's query, ensuring that all necessary context is provided.
    
    **Step 6.4**. Find the TODO comment: "Extract and return the response" and add this code snippet:
    
    ```python
        return response["output"]
    ```
    
    This code extracts the relevant response information from the agent's output, which typically comes as a dictionary with multiple fields.
    
    **Step 6.5**. Find the TODO comment: "Implement error handling" and add this code snippet:
    
    ```python
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        return f"Error: {str(e)}"
    ```
    
    This code implements robust error handling to gracefully manage various failure scenarios that might occur during processing, such as API failures or invalid user inputs.


## Testing Your Implementation

After completing each task, you can test your implementation using the provided app.py:

```bash
python app.py
```

This will present you with a menu to:
1. Run a demo that tests all the core functionality
2. Launch an interactive news agent CLI
3. Exit the application

Use these options to verify that your implementations work correctly. The demo mode is particularly useful for quick validation of all components.

## Conclusion

In this hands-on activity, you've built a `NewsAgent` system that integrates LLMs with an external news API. By implementing secure API authentication, resilient error handling, effective caching, and rate limiting mechanisms, you've created an agent that reliably processes news articles while gracefully handling common API integration challenges. The modular architecture you've developed separates concerns between API interaction, data processing, and LLM integration, making the system maintainable and extensible.

Through the LangChain framework, you've experienced how to orchestrate complex interactions between language models and external data sources using tools, chains, middleware, and agents. These skills are directly applicable to real-world LLM application development, where connecting AI models with dynamic data is essential for building production-ready systems. The resilience patterns you've implemented—from circuit breakers to multi-tier fallback strategies—will serve as foundational techniques for creating robust AI systems that users can depend on.