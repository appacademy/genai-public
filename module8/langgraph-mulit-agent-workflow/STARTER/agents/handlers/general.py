from models.state import AgentState
from langchain_core.messages import AIMessage


def handle_general_inquiry(
    state: AgentState, ollama_client, knowledge_base
) -> AgentState:
    """Handles general inquiries that don't fit other categories."""
    # TODO: Implement this handler following the pattern of the billing handler,
    # but customized for general inquiries. Remember to:

    # TODO: Extract information from the current message

    # TODO: Create personalized greeting and context acknowledgment

    # TODO: Get general context from the knowledge base

    # TODO: Create the prompt for the AI model

    # TODO: Generate the response using the Ollama client

    # TODO: Update the message status and history

    # TODO: Return the updated state

    return state
