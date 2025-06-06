from typing import Dict
from langgraph.graph import StateGraph, END
from models.state import AgentState
from agents.classifier import classify_message
from agents.router import route_message
from agents.handlers.billing import handle_billing_inquiry
from agents.handlers.technical import handle_technical_inquiry
from agents.handlers.product import handle_product_inquiry
from agents.handlers.general import handle_general_inquiry
from agents.handlers.priority import handle_priority_inquiry
from langchain_core.messages import HumanMessage


def create_customer_service_workflow(ollama_client, knowledge_base):
    """Builds and returns the complete workflow graph."""
    workflow = StateGraph(AgentState)

    # Add nodes to the graph with dependencies injected
    workflow.add_node(
        "classifier", lambda state: classify_message(state, ollama_client)
    )
    workflow.add_node("router", route_message)
    workflow.add_node(
        "billing_handler",
        lambda state: handle_billing_inquiry(state, ollama_client, knowledge_base),
    )
    workflow.add_node(
        "technical_handler",
        lambda state: handle_technical_inquiry(state, ollama_client, knowledge_base),
    )
    workflow.add_node(
        "product_handler",
        lambda state: handle_product_inquiry(state, ollama_client, knowledge_base),
    )
    workflow.add_node(
        "general_handler",
        lambda state: handle_general_inquiry(state, ollama_client, knowledge_base),
    )
    workflow.add_node(
        "priority_handler",
        lambda state: handle_priority_inquiry(state, ollama_client, knowledge_base),
    )

    # Define the edges in the graph
    workflow.add_edge("classifier", "router")

    # Conditional edges from router to specialized handlers
    workflow.add_conditional_edges(
        "router",
        lambda x: x["next"],
        {
            "billing": "billing_handler",
            "technical": "technical_handler",
            "product": "product_handler",
            "general": "general_handler",
            "priority_handling": "priority_handler",
        },
    )

    # All handlers lead to END
    workflow.add_edge("billing_handler", END)
    workflow.add_edge("technical_handler", END)
    workflow.add_edge("product_handler", END)
    workflow.add_edge("general_handler", END)
    workflow.add_edge("priority_handler", END)

    # Set the entry point
    workflow.set_entry_point("classifier")

    # Compile the graph
    return workflow.compile()


def process_inquiry(
    message_content: str,
    user_name: str = None,
    user_email: str = None,
    additional_context: str = None,
    ollama_client=None,
    knowledge_base=None,
) -> Dict:
    """
    Processes a customer inquiry through the workflow.
    Returns the final state after processing.
    """
    # Initialize workflow
    workflow = create_customer_service_workflow(ollama_client, knowledge_base)

    # Create initial state
    initial_state = AgentState(
        messages=[HumanMessage(content=message_content)],
        current_message={
            "content": message_content,
            "type": None,
            "priority": None,
            "status": "new",
            "user_name": user_name,
            "user_email": user_email,
            "additional_context": additional_context,
        },
        history=[],
    )

    # Execute workflow
    result = workflow.invoke(initial_state)

    return result
