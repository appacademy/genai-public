import logging
from .system import HighAvailabilityRAG  # Relative import

logger = logging.getLogger("HighAvailabilityRAG.TestRunner")


def test_high_availability_rag():
    """Test the HighAvailabilityRAG with simulated failures interactively"""
    rag = HighAvailabilityRAG()
    run_count = 0

    while True:  # Outer loop to allow re-running tests
        run_count += 1
        print(f"\n--- Starting Test Run #{run_count} ---")
        # Process several queries to demonstrate fallbacks
        queries = [
            "How do RAG systems work?",
            "What are the advantages of Docker containers?",
            "Explain circuit breaker patterns",
            "How to implement fallback strategies?",
            "What is graceful degradation?",
        ]

        for query in queries:
            print("\n" + "=" * 80)
            print(f"QUERY: {query}")
            print("=" * 80)

            response = rag.query(query)

            print("\nRESPONSE:")
            print(response)

            # Print current system health
            health = rag.get_system_health()
            print("\nSYSTEM HEALTH:")
            for component, metrics in health.items():
                print(f"  {component.upper()}:")
                for metric, value in metrics.items():
                    if isinstance(value, float):
                        print(f"    {metric}: {value:.3f}")
                    else:
                        print(f"    {metric}: {value}")

            # --- Interactive Question Loop for All Circuit Breakers ---
            components = ["embedder", "retriever", "generator"]
            all_correct = False

            while not all_correct:
                print("\n---")
                print(
                    "For each circuit breaker, enter its current state (closed/open/half_open) or 'skip' to move on:"
                )

                # Track correctness for each component
                correct_answers = 0

                for component in components:
                    expected_state = health[component]["state"]  # Get the actual state
                    user_answer = (
                        input(
                            f"What is the current state of the {component.upper()} circuit breaker? "
                        )
                        .lower()
                        .strip()
                    )

                    if user_answer == "skip":
                        print("Skipping remaining questions...")
                        all_correct = True  # Force exit from the loop
                        break  # Exit the component loop

                    if user_answer == expected_state:
                        print(
                            f"✓ Correct! The {component.upper()} circuit breaker is {expected_state}."
                        )
                        correct_answers += 1
                    else:
                        print(
                            f"✗ Not quite. The {component.upper()} circuit breaker is {expected_state}."
                        )

                # Check if all answers were correct or if we're skipping
                if correct_answers == len(components):
                    all_correct = True
                    print(
                        "\nGreat job! You correctly identified the state of all circuit breakers."
                    )
                elif not all_correct and user_answer != "skip":
                    print(
                        "\nLet's try again. Check the SYSTEM HEALTH output above for the current states."
                    )
                    retry = (
                        input("Press Enter to retry or type 'skip' to move on: ")
                        .lower()
                        .strip()
                    )
                    if retry == "skip":
                        all_correct = True  # Force exit from the loop

            # Pause before moving to next query
            if user_answer != "skip":
                input("Press Enter to continue to the next query...")
            # --- End Interactive Question Loop ---
        # --- End of inner for loop ---

        # --- Ask if user wants to run again (Correctly indented inside the outer while loop) ---
        print("\n" + "=" * 80)
        repeat = input("Run tests again? (yes/no): ").lower().strip()
        if repeat != "yes":
            break  # Exit the outer while loop
    # --- End of outer while loop ---

    print("\nTesting finished!")
