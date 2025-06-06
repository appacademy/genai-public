from typing import Dict, Any
from agents.base_agent import Agent
from models.data_models import AgentResponse

# TODO: Study this research agent implementation as your reference model
# Notice how this agent:
# - Safely extracts the problem using inputs.get() with a default value
# - Creates a detailed system prompt that clearly defines the agent's role and output format
# - Combines the system prompt with a targeted user prompt that incorporates the problem
# - Returns a properly structured AgentResponse with content, confidence, and metadata
#
# You'll follow this pattern when implementing the planning, analysis, and solution agents
# in the upcoming tasks. Focus on understanding how each component contributes to the
# overall agent functionality.


class ResearchAgent(Agent):
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:

        # Input Extraction
        problem = inputs.get("problem", "")

        # System Prompt Construction
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

        # LLM Interaction
        research_results = self._call_llm(system_prompt, user_prompt)

        # Response Formatting
        return AgentResponse(
            content=research_results,
            confidence=0.8,
            metadata={"source": "research_agent", "problem": problem},
        )
