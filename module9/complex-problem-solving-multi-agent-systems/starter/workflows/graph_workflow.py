from typing import Dict, Any, Literal
from typing_extensions import TypedDict
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END, START
from models.data_models import ProblemSolvingState
from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.solution_agent import SolutionAgent
from agents.review_agent import CriticalReviewAgent
from utils.markdown_writer import MarkdownWriter
import time
import os

# Initialize agents
research_agent = ResearchAgent()
analysis_agent = AnalysisAgent()
solution_agent = SolutionAgent()
review_agent = CriticalReviewAgent()


# Create a global markdown writer that will be initialized in solve_problem_with_graph
markdown_writer = None


# TODO: Implement all four agent functions (run_research, run_analysis, run_solution, run_review)
# Each function should:
# - Extract necessary information from state
# - Call the appropriate agent
# - Update the markdown writer
# - Return updated state values


# Define the agent functions that work with the graph state
def run_research(state: ProblemSolvingState) -> Dict[str, Any]:
    # TODO: Implement the run_research function

    # TODO: 1. Print a message indicating the Research Agent is working

    # TODO: 2. Extract the problem from the state

    # TODO: 3. Call the research_agent with the problem

    # TODO: 4. Print the confidence score of the response

    # TODO: 5. Add the research results to the markdown writer

    # TODO: 6. Return a dictionary with the research_results key

    return None  # Replace with actual implementation


def run_analysis(state: ProblemSolvingState) -> Dict[str, Any]:
    # TODO: Implement the run_analysis function

    # TODO: Print a message indicating the Analysis Agent is working

    # TODO: Extract the problem and research_results from the state

    # TODO: Call the analysis_agent with the problem and research_results

    # TODO: Print the confidence score of the response

    # TODO: Add the analysis results to the markdown writer

    # TODO: Return a dictionary with the analysis_results key

    return None  # Replace with actual implementation


def run_solution(state: ProblemSolvingState) -> Dict[str, Any]:
    # TODO: Implement the run_solution function

    # TODO: 1. Print a message indicating the Solution Agent is working (include iteration number)

    # TODO: 2. Extract the problem, research_results, analysis_results, and critique from the state

    # TODO: 3. Call the solution_agent with all the extracted information

    # TODO: 4. Print the confidence score of the response

    # TODO: 5. Add the solution to the markdown writer (with appropriate section title based on iteration)

    # TODO: 6. Return a dictionary with the solution key

    return None  # Replace with actual implementation


def run_review(state: ProblemSolvingState) -> Dict[str, Any]:
    # TODO: Implement the run_review function

    # TODO: Print a message indicating the Critical Review Agent is evaluating the solution

    # TODO: Extract the problem, research_results, analysis_results, and solution from the state

    # TODO: Call the review_agent with all the extracted information

    # TODO: Extract the recommendation from the response metadata

    # TODO: Print the recommendation

    # TODO: Add the critique to the markdown writer

    # TODO: Return a dictionary with the critique and recommendation keys

    return None  # Replace with actual implementation


# TODO: Implement the should_continue function that creates the adaptive feedback loop
# Define the routing logic
def should_continue(state: ProblemSolvingState) -> Literal["solution_node", "end_node"]:
    # TODO: Implement the should_continue function
    # 1. Extract the recommendation and iteration from the state
    # 2. Determine whether to continue with another solution iteration or end the workflow
    # 3. Return "end_node" if the recommendation is "Accept" or the iteration count is >= 1
    # 4. Return "solution_node" otherwise
    # 5. Print appropriate messages based on the decision

    return "end_node"  # Replace with actual implementation


# Create the graph
def build_problem_solving_graph():
    # TODO: Implement the build_problem_solving_graph function

    # TODO: Create a new StateGraph with the ProblemSolvingState type

    # TODO: Add all the agent nodes (research, analysis, solution_node, review, end_node)

    # TODO: Add the edges to connect the nodes in the correct sequence

    # TODO: Add conditional edges based on the should_continue function

    # TODO: Compile and return the graph

    return None  # Replace with actual implementation


def solve_problem_with_graph(problem: str) -> Dict[str, Any]:
    """
    Solve a problem using the LangGraph workflow

    Args:
        problem: The problem statement to solve

    Returns:
        Dict containing the final state with the solution
    """
    # TODO: Initialize the markdown writer with the problem statement

    # TODO: Build the problem-solving graph if not already initialized

    # TODO: Create the initial state with the problem and set iteration to 1

    # TODO: Print a message indicating the problem-solving process is starting

    # TODO: Execute the graph with appropriate recursion limit settings

    # TODO: Add the final solution to the markdown report

    # TODO: Save the markdown report to a file and print the output path

    # TODO: Format and return the results dictionary with all components:
    # - problem statement
    # - research results
    # - analysis results
    # - solution history (including iterations, solutions, critiques, and recommendations)
    # - final solution
    # - final critique
    # - recommendation
    # - markdown file path

    return {}  # Replace with actual implementation
