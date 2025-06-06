from models.state import AgentState
from langchain_core.messages import AIMessage


def handle_priority_inquiry(
    state: AgentState, ollama_client, knowledge_base
) -> AgentState:
    """Handles urgent inquiries with special priority treatment."""
    # TODO: Implement this handler following the pattern of the billing handler,
    # but customized for urgent priority inquiries. Remember to:

    # TODO: Extract message information

    # TODO: Get knowledge base context

    # TODO: Create prompt for urgent cases

    # TODO: Generate and format response

    # TODO: Update state with response and status

    return state
