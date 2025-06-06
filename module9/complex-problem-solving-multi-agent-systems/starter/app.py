import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv
from workflows.graph_workflow import solve_problem_with_graph

# Load environment variables
load_dotenv()


def display_menu():
    """Display the main menu options"""
    print("\n===== Multi-Agent Problem Solving System =====")
    print("1. Run Demo (using sample problem)")
    print("2. Run Interactive Problem Solving")
    print("3. Exit")
    return input("Select an option (1-3): ")


def demo_problem():
    """Run a demonstration using the sample problem"""
    problem = """
    A mid-sized technology company is experiencing high employee turnover, 
    particularly among their software development team. The company wants to 
    understand the root causes and develop a comprehensive strategy to improve 
    retention without significantly increasing compensation costs.
    """

    print("\n==== Running Demo with LangGraph Workflow ====\n")
    results = solve_problem_with_graph(problem)

    # Display final solution
    print("\n" + "=" * 50)
    print("FINAL SOLUTION:")
    print("=" * 50)
    print(results["final_solution"])
    print("\n" + "=" * 50)

    # Display markdown path if available
    if "markdown_path" in results:
        print(f"\n📝 Detailed report saved to: {results['markdown_path']}")

    print("\n==== End of Demo ====\n")


def interactive_mode():
    """Run the system with a user-provided problem"""
    print("\n==== Interactive Problem Solving ====")
    print("Please describe the problem you'd like to solve:")
    problem = input("> ")

    if not problem.strip():
        print("Problem description cannot be empty. Returning to main menu.")
        return

    print("\n==== Running with LangGraph Workflow ====\n")
    results = solve_problem_with_graph(problem)

    # Display final solution
    print("\n" + "=" * 50)
    print("FINAL SOLUTION:")
    print("=" * 50)
    print(results["final_solution"])
    print("\n" + "=" * 50)

    # Display markdown path if available
    if "markdown_path" in results:
        print(f"\n📝 Detailed report saved to: {results['markdown_path']}")


def main():
    """Main application entry point"""
    while True:
        choice = display_menu()

        if choice == "1":
            demo_problem()
        elif choice == "2":
            interactive_mode()
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please select 1, 2, or 3.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
