from typing import Dict, Any
from agents.base_agent import Agent
from models.data_models import AgentResponse


class AnalysisAgent(Agent):
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:
        problem = inputs.get("problem", "")
        research_results = inputs.get("research_results", "")

        system_prompt = """
        You are a specialized analysis agent. Your job is to process research findings and identify:
        1. Core issues within the problem
        2. Relationships between different aspects of the problem
        3. Potential approaches to solving the problem
        4. Priority areas to address
        
        Structure your analysis with the following sections:
        - Core Issues (prioritized)
        - Relationships and Dependencies
        - Potential Approaches
        - Recommended Focus Areas
        """

        user_prompt = f"""
        Problem: {problem}
        
        Research Results:
        {research_results}
        
        Please analyze this information and provide your insights.
        """

        analysis_results = self._call_llm(system_prompt, user_prompt)

        return AgentResponse(
            content=analysis_results,
            confidence=0.7,
            metadata={"source": "analysis_agent"},
        )
