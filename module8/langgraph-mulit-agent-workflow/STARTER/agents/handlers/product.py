from models.state import AgentState
from langchain_core.messages import AIMessage


def handle_product_inquiry(
    state: AgentState, ollama_client, knowledge_base
) -> AgentState:
    """Handles product-related inquiries."""
    # TODO: Implement this handler following the pattern of the billing handler,
    # but customized for product inquiries. Remember to:

    # TODO: Extract information from current message

    # TODO: Get product context from knowledge base

    # TODO: Create response prompt with product context

    # TODO: Generate response using Ollama

    # TODO: Update state with response and message status

    # TODO: Return updated state
