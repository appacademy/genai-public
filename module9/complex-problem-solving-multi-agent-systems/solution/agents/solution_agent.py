from typing import Dict, Any
from agents.base_agent import Agent
from models.data_models import AgentResponse


class SolutionAgent(Agent):
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:
        problem = inputs.get("problem", "")
        research_results = inputs.get("research_results", "")
        analysis_results = inputs.get("analysis_results", "")
        previous_critique = inputs.get("previous_critique", "")

        system_prompt = """
        You are a specialized solution generation agent. Your job is to propose comprehensive 
        solutions to the problem based on research and analysis.
        
        Create a detailed solution with the following components:
        1. Executive Summary
        2. Proposed Solutions (with rationale for each)
        3. Implementation Steps
        4. Expected Outcomes
        5. Potential Challenges
        6. Success Metrics
        
        If you've received previous critique, make sure to address those points in your updated solution.
        """

        user_prompt = f"""
        Problem: {problem}
        
        Research Results:
        {research_results}
        
        Analysis:
        {analysis_results}
        
        Previous Critique (if any):
        {previous_critique}
        
        Please generate a comprehensive solution to this problem.
        """

        solution = self._call_llm(system_prompt, user_prompt)

        # Adjust confidence based on whether this is an iteration after critique
        confidence = 0.9 if previous_critique else 0.75

        return AgentResponse(
            content=solution,
            confidence=confidence,
            metadata={
                "source": "solution_agent",
                "iteration": 1 if not previous_critique else 2,
            },
        )
