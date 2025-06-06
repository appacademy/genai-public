from typing import Dict, Any
from agents.base_agent import Agent
from models.data_models import AgentResponse


class CriticalReviewAgent(Agent):
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:
        # TODO: Implement the process method that:
        # 1. Extract problem, research_results, analysis_results, and proposed_solution from inputs
        # 2. Define the system prompt for the critical review agent
        # 3. Create a user prompt that includes all the extracted information
        # 4. Call the LLM using self._call_llm
        # 5. Extract the recommendation (Accept, Revise, or Reject) from the critique
        # 6. Return an AgentResponse with the critique, confidence score, and metadata including the recommendation

        # TODO: Extract all required inputs from the inputs dictionary
        
        # TODO: Define the system prompt for the critical review agent
        
        # TODO: Create a user prompt that includes all the extracted information        
        
        # TODO: Call the LLM using self._call_llm
        
        # TODO: Extract recommendation using a simple heuristic
        # Look for "Accept", "Revise", or "Reject" in the last 100 characters of the critique
        # Default to "Revise" if no clear recommendation is found
        
        # TODO: Return an AgentResponse with the critique, confidence score, and metadata
        # Include source and recommendation in the metadata