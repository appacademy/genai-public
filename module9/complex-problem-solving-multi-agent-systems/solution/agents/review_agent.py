from typing import Dict, Any
from agents.base_agent import Agent
from models.data_models import AgentResponse


class CriticalReviewAgent(Agent):
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:
        problem = inputs.get("problem", "")
        research_results = inputs.get("research_results", "")
        analysis_results = inputs.get("analysis_results", "")
        proposed_solution = inputs.get("proposed_solution", "")

        system_prompt = """
        You are a specialized critical review agent. Your job is to carefully evaluate 
        proposed solutions and identify:
        
        1. Gaps or missing considerations
        2. Logical inconsistencies
        3. Implementation challenges
        4. Alternative approaches that might be superior
        5. Strengths of the current solution
        
        Be constructive but thorough in your critique. Structure your review with:
        - Solution Strengths
        - Critical Gaps
        - Inconsistencies
        - Implementation Concerns
        - Suggested Improvements
        
        End with an overall assessment and a clear recommendation: 
        Accept, Revise, or Reject the proposed solution.
        """

        user_prompt = f"""
        Problem: {problem}
        
        Research Results:
        {research_results}
        
        Analysis:
        {analysis_results}
        
        Proposed Solution:
        {proposed_solution}
        
        Please provide a critical review of this solution.
        """

        critique = self._call_llm(system_prompt, user_prompt)

        # Extract recommendation using a simple heuristic
        recommendation = "Revise"  # Default
        if "Accept" in critique[-100:]:
            recommendation = "Accept"
        elif "Reject" in critique[-100:]:
            recommendation = "Reject"

        return AgentResponse(
            content=critique,
            confidence=0.85,
            metadata={
                "source": "critical_review_agent",
                "recommendation": recommendation,
            },
        )
