import sys
import os
from dotenv import load_dotenv
from ollama_client import OllamaClient
from knowledge.knowledge_base import KnowledgeBase
from workflow import process_inquiry
from ui.console import run_interactive_console

# Load environment variables
load_dotenv()
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")

# Initialize Ollama client
ollama_client = OllamaClient(OLLAMA_API_URL)

# Initialize the knowledge base
knowledge_base = KnowledgeBase()


def main():
    """Main entry point for the application."""
    try:
        # Create a process_inquiry function with dependencies injected
        def process_inquiry_with_deps(
            message_content, user_name=None, user_email=None, additional_context=None
        ):
            return process_inquiry(
                message_content,
                user_name,
                user_email,
                additional_context,
                ollama_client,
                knowledge_base,
            )

        # Check if we should run in demo mode
        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            # Import and run the demo with predefined examples
            from ui.demo import run_demo

            print("\n=== Running demo with example inquiries ===")
            run_demo(process_inquiry_with_deps)
        else:
            # Run in interactive console mode
            run_interactive_console(process_inquiry_with_deps)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
