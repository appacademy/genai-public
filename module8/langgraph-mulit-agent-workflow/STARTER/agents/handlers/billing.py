from models.state import AgentState
from langchain_core.messages import AIMessage


def handle_billing_inquiry(
    state: AgentState, ollama_client, knowledge_base
) -> AgentState:
    """Handles billing-related inquiries."""
    # TODO: 1. Extract message details (content, priority, user info) from state

    # TODO: 2. Create personalized greeting if user name is provided

    # TODO: 3. Get billing-specific context from the knowledge base

    # TODO: 4. Add priority note for high-priority inquiries

    # TODO: 5. Create a detailed prompt including:
    #    - Billing context from knowledge base
    #    - Customer inquiry
    #    - Instructions for personalization

    # TODO: 6. Generate a response using ollama_client

    # TODO: 7. Ensure the response includes Emma G.'s signature

    # TODO: 8. Update message status to "resolved"

    # TODO: 9. Add the message to history

    # TODO: 10. Add the AI response to messages

    return state
