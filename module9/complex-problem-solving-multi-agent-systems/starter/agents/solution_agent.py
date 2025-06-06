from typing import Dict, Any
from agents.base_agent import Agent
from models.data_models import AgentResponse


class SolutionAgent(Agent):
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:
        # TODO: Implement the process method that:
        # 1. Extract problem, research_results, analysis_results, and previous_critique from inputs
        # 2. Use the existing system prompt
        # 3. Create a user prompt that includes all the extracted information
        # 4. Call the LLM using self._call_llm
        # 5. Implement adaptive confidence scoring based on whether this is an iteration
        # 6. Return an AgentResponse with the solution, confidence score, and metadata

        # TODO: Extract all required inputs from the inputs dictionary
        
        # TODO: Define the system prompt
        
        # TODO: Create a user prompt that includes all the extracted information
        
        # TODO: Call the LLM using self._call_llm
        
        # TODO: Implement adaptive confidence scoring based on whether this is an iteration
        # Confidence should be 0.9 if there's a previous critique, otherwise 0.75
        
        # TODO: Return an AgentResponse with the solution, confidence score, and metadata
        # Include source and iteration information in the metadata