from models.state import AgentState
from langchain_core.messages import AIMessage


def handle_technical_inquiry(
    state: AgentState, ollama_client, knowledge_base
) -> AgentState:
    """Handles technical-related inquiries."""
    # TODO: Implement this handler following the pattern of the billing handler,
    # but customized for technical inquiries. Remember to:
    # - Get technical context from the knowledge base
    # - Include personalization and Emma G. signature
    # - Update the message status and history

    # TODO: Extract message details

    # TODO: Create personalized greeting and context acknowledgment

    # TODO: Get technical context from knowledge base

    # TODO: Create response prompt

    # TODO: Generate response and ensure proper signature

    # TODO: Update state with response and message status

    return state
