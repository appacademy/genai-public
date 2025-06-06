from typing import Dict, Any
from agents.base_agent import Agent
from models.data_models import AgentResponse


class ResearchAgent(Agent):
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:
        problem = inputs.get("problem", "")

        system_prompt = """
        You are a specialized research agent responsible for gathering key information about a problem.
        Your goal is to identify:
        1. Key facts relevant to the problem
        2. Important context or background information
        3. Potential resources or references that might help solve the problem
        
        Provide your research in a clear, structured format with sections for:
        - Key Facts
        - Contextual Information
        - Potential Resources
        - Initial Hypotheses
        """

        user_prompt = f"I need you to research the following problem: {problem}"

        research_results = self._call_llm(system_prompt, user_prompt)

        return AgentResponse(
            content=research_results,
            confidence=0.8,
            metadata={"source": "research_agent", "problem": problem},
        )
