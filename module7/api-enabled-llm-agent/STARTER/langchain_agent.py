"""
LangChain agent implementation for the NewsAgent application.
Integrates with Ollama to use the Gemma 3 4B model.

This implementation uses LangChain as the central orchestration layer,
with tools, chains, and middleware for resilient API operations.
"""

import logging
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.llms.ollama import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Import our LangChain components
from langchain_tools import (
    GetHeadlinesTool,
    SearchNewsTool,
    SummarizeArticleTool,
    CategorizeArticleTool,
)
from langchain_chains import (
    create_llm,
    summarization_chain,
    categorization_chain,
    multi_processing_chain,
)
from langchain_middleware import with_resilience

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")


class NewsAgentLangChain:
    """
    LangChain-based news agent application.
    Uses LangChain tools, chains, and middleware for resilient API operations.
    """

    def __init__(self):
        """Initialize the LangChain agent with tools and chains."""
        # Initialize Ollama LLM with Gemma 3 4B
        self.llm = create_llm(temperature=0.7, model="gemma3:4b")

        # Initialize tools
        self.tools = self._create_tools()

        # Set up memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        # Create the agent
        self.agent = self._create_agent()

        logger.info("LangChain NewsAgent initialized successfully")

    def _create_tools(self) -> List[Tool]:
        """Create LangChain tools for news operations."""
        # Initialize the tool instances
        headlines_tool = GetHeadlinesTool()
        search_tool = SearchNewsTool()
        summarize_tool = SummarizeArticleTool()
        categorize_tool = CategorizeArticleTool()

        # Convert to LangChain Tool format
        tools = [
            Tool.from_function(
                func=headlines_tool._run,
                name="get_headlines",
                description=headlines_tool.description,
            ),
            Tool.from_function(
                func=search_tool._run,
                name="search_news",
                description=search_tool.description,
            ),
            Tool.from_function(
                func=summarize_tool._run,
                name="summarize_article",
                description=summarize_tool.description,
            ),
            Tool.from_function(
                func=categorize_tool._run,
                name="categorize_article",
                description=categorize_tool.description,
            ),
        ]

        return tools

    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent with the defined tools and LLM."""
        # TODO: Implement the LangChain ReAct agent

        # TODO: Create a prompt template that includes tools, chat history, and agent_scratchpad

        # TODO: Create the ReAct agent using create_react_agent with the LLM, tools, and prompt

        # TODO: Create the agent executor with appropriate parameters

        # TODO: Return the configured agent executor

    def run(self, query: str) -> str:
        """
        Run the agent with a user query.

        Args:
            query: User input

        Returns:
            Agent response
        """
        # TODO: Task 6 - Implement User Query Processing

        # TODO: Log the user query

        # TODO: Invoke the LangChain agent with the query

        # TODO: Extract and return the response

        # TODO: Implement error handling
