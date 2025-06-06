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


# Define the agent functions that work with the graph state
def run_research(state: ProblemSolvingState) -> Dict[str, Any]:
    print("📚 Research Agent working...")
    problem = state.problem
    response = research_agent.process({"problem": problem})

    print(f"Research complete with confidence: {response.confidence:.2f}\n")

    # Add to markdown
    if markdown_writer:
        markdown_writer.add_section("Research Phase", response.content)

    return {"research_results": response.content}


def run_analysis(state: ProblemSolvingState) -> Dict[str, Any]:
    print("🧩 Analysis Agent working...")
    problem = state.problem
    research_results = state.research_results

    response = analysis_agent.process(
        {"problem": problem, "research_results": research_results}
    )

    print(f"Analysis complete with confidence: {response.confidence:.2f}\n")

    # Add to markdown
    if markdown_writer:
        markdown_writer.add_section("Analysis Phase", response.content)

    return {"analysis_results": response.content}


def run_solution(state: ProblemSolvingState) -> Dict[str, Any]:
    iteration = state.iteration
    print(f"💡 Solution Agent working (iteration {iteration})...")

    problem = state.problem
    research_results = state.research_results
    analysis_results = state.analysis_results
    previous_critique = state.critique

    response = solution_agent.process(
        {
            "problem": problem,
            "research_results": research_results,
            "analysis_results": analysis_results,
            "previous_critique": previous_critique,
        }
    )

    print(f"Solution generated with confidence: {response.confidence:.2f}\n")

    # Add to markdown
    if markdown_writer:
        # Simplify heading if there's only one iteration
        if iteration == 1:
            section_title = "Solution Phase"
        else:
            section_title = f"Solution Phase (Iteration {iteration})"

        markdown_writer.add_section(section_title, response.content)

    return {"solution": response.content}


def run_review(state: ProblemSolvingState) -> Dict[str, Any]:
    print(f"🔍 Critical Review Agent evaluating solution...")

    problem = state.problem
    research_results = state.research_results
    analysis_results = state.analysis_results
    solution = state.solution

    response = review_agent.process(
        {
            "problem": problem,
            "research_results": research_results,
            "analysis_results": analysis_results,
            "proposed_solution": solution,
        }
    )

    recommendation = response.metadata.get("recommendation", "Revise")
    print(f"Review complete - Recommendation: {recommendation}\n")

    # Add to markdown
    if markdown_writer:
        markdown_writer.add_section("Review Phase", response.content)

    return {"critique": response.content, "recommendation": recommendation}


# Define the routing logic
def should_continue(state: ProblemSolvingState) -> Literal["solution_node", "end_node"]:
    recommendation = state.recommendation
    iteration = state.iteration

    # Strict termination after exactly 1 iteration (which means 2 total iterations since we start at 1)
    if recommendation == "Accept" or iteration >= 1:
        # Final solution is the current solution
        print(
            f"✅ Problem solving complete after {iteration + 1} iterations! Final recommendation: {recommendation}"
        )
        return "end_node"
    else:
        # Increment iteration counter
        print(f"⟳ Starting iteration {iteration + 1} (final iteration)...")
        return "solution_node"


# Create the graph
def build_problem_solving_graph():
    # Create a new graph
    workflow = StateGraph(ProblemSolvingState)

    # Add all the agent nodes
    workflow.add_node("research", run_research)
    workflow.add_node("analysis", run_analysis)
    workflow.add_node("solution_node", run_solution)
    workflow.add_node("review", run_review)
    workflow.add_node("end_node", lambda x: x)  # Identity function as a terminal node

    # Add the edges - how the agents connect to each other
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "analysis")
    workflow.add_edge("analysis", "solution_node")
    workflow.add_edge("solution_node", "review")
    workflow.add_conditional_edges("review", should_continue)
    workflow.add_edge("end_node", END)

    # Compile the graph
    return workflow.compile()


# Main function to execute the graph workflow
def solve_problem_with_graph(problem: str) -> Dict[str, Any]:
    """
    Solve a problem using the LangGraph workflow

    Args:
        problem: The problem statement to solve

    Returns:
        Dict containing the final state with the solution
    """
    global markdown_writer

    # Initialize markdown writer
    markdown_writer = MarkdownWriter(problem)

    # Initialize graph if not already done
    graph = build_problem_solving_graph()

    # Initial state
    initial_state = ProblemSolvingState(problem=problem, iteration=1)

    print(f"🔍 Starting to solve problem: {problem[:50]}...\n")

    # Execute the graph with increased recursion limit
    result = graph.invoke(initial_state, {"recursion_limit": 50})

    # Add final solution to markdown
    if result.get("final_solution"):
        markdown_writer.add_section("Final Solution", result.get("final_solution", ""))
    else:
        markdown_writer.add_section("Final Solution", result.get("solution", ""))

    # Save markdown to file
    output_path = markdown_writer.save()
    print(f"\n✅ Markdown report saved to: {output_path}")

    # Format the output similar to the orchestrator for compatibility
    formatted_result = {
        "problem": problem,
        "research": result.get("research_results", ""),
        "analysis": result.get("analysis_results", ""),
        "solution_history": [
            {
                "iteration": i + 1,
                "solution": result.get("solution", ""),
                "critique": result.get("critique", ""),
                "recommendation": result.get("recommendation", ""),
            }
            for i in range(result.get("iteration", 1))
        ],
        "final_solution": result.get("final_solution", ""),
        "final_critique": result.get("critique", ""),
        "recommendation": result.get("recommendation", ""),
        "markdown_path": output_path,
    }

    return formatted_result
