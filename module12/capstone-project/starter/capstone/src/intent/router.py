from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Intent(BaseModel):
    intent: str = Field(description="The classified intent of the user query")
    args: Optional[Dict[str, Any]] = Field(
        None, description="Additional arguments extracted from the query"
    )


class IntentRouter:
    # TODO: Implement the IntentRouter class to classify user queries into specific intents
    
    # TODO: Implement the __init__ method to initialize the LLM and the prompt template
    def __init__(self, llm):
        # TODO: Initialize the LLM and the parser
        
        # TODO: Create a prompt template for intent classification
        
        # TODO: Create a chain that combines the prompt, LLM, and parser

    # TODO: Implement the classify method to classify user queries into specific intents
    def classify(self, query):
        """Classify a user query into an intent"""
        