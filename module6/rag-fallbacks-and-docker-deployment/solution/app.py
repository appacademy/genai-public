# Main entry point for the High Availability RAG Simulation

# Configure logging (needs to be done before other imports that might log)
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Import the test runner function from the new package structure
from ha_rag_simulation.test_runner import test_high_availability_rag

if __name__ == "__main__":
    # Execute the interactive test simulation
    test_high_availability_rag()
