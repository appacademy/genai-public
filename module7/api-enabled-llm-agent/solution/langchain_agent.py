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

        # Create the ReAct agent
        agent = create_react_agent(self.llm, self.tools, prompt)

        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
        )

        return agent_executor

    def run(self, query: str) -> str:
        """
        Run the agent with a user query.

        Args:
            query: User input

        Returns:
            Agent response
        """
        try:
            logger.info(f"Processing user query: {query}")
            response = self.agent.invoke({"input": query})
            return response["output"]
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            return f"Error: {str(e)}"
