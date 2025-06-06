from typing import Dict, Any
from agents.base_agent import Agent
from models.data_models import AgentResponse


class AnalysisAgent(Agent):
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:
        # TODO: Implement the process method that:
        # 1. Extract both problem and research_results from inputs
        # 2. Define a system prompt for the analysis agent
        # 3. Create a user prompt that includes the problem and research results
        # 4. Call the LLM using self._call_llm
        # 5. Return an AgentResponse with the analysis results, confidence score, and metadata

        # TODO: Extract problem and research_results from the inputs dictionary
        
        # TODO: Define the system prompt for the analysis agent
		
        # TODO: Create a user prompt that includes the problem and research results
        
        # TODO: Call the LLM using self._call_llm
        
        # TODO: Return an AgentResponse with the analysis results, confidence score, and metadata