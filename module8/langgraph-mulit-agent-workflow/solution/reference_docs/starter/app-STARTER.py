from typing import Annotated, List, Literal, TypedDict, Union, Dict, Optional
from langchain_core.messages import HumanMessage, AIMessage
import operator
import os
from dotenv import load_dotenv
import json
from langgraph.graph import StateGraph, END
from ollama_client import OllamaClient

# Load environment variables
load_dotenv()
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")

# Initialize Ollama client
ollama_client = OllamaClient(OLLAMA_API_URL)

# Define our message types and state
class Message(TypedDict):
    content: str
    type: Optional[str]
    priority: Optional[int]
    status: Optional[str]

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]
    current_message: Message
    history: List[Message]

def classify_message(state: AgentState) -> AgentState:
    """
    Analyzes the incoming message to determine its type and priority.
    Types can be: billing, technical, product, general
    Priority can be: 1 (urgent), 2 (high), 3 (medium), 4 (low)
    """
    # TODO:
    # - Extract the current message and content from the state
    # - Create a prompt for the classifier asking the LLM to determine message type and priority
    # - Invoke the LLM with the classification prompt
    # - Parse the JSON response and update the current message with type and priority
    # - Handle any JSON parsing errors by setting default values
    # - Update the state with the classification results
    # - Add a classification message to the messages list
    
    # Stub to make code runnable
    current_message = state["current_message"]
    current_message["type"] = "general"
    current_message["priority"] = 4
    current_message["status"] = "classified"
    state["current_message"] = current_message
    state["messages"].append(
        AIMessage(content=f"Message classified as {current_message['type']} with priority {current_message['priority']}")
    )
    return state

def handle_billing_inquiry(state: AgentState) -> AgentState:
    """Handles billing-related inquiries."""
    # TODO:
    # - Extract the current message, content, and priority from the state
    # - Create a prompt for the billing specialist, noting high priority if needed
    # - Invoke the LLM with the billing-specific prompt to get a response
    # - Update the message status to "resolved"
    # - Add the message to history
    # - Add the LLM response to the messages list
    
    # Stub to make code runnable
    current_message = state["current_message"]
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    state["history"].append(current_message)
    state["messages"].append(AIMessage(content="This is a placeholder billing response."))
    return state

def handle_technical_inquiry(state: AgentState) -> AgentState:
    """Handles technical support inquiries."""
    # TODO:
    # - Extract the current message, content, and priority from the state
    # - Create a prompt for the technical support specialist, noting high priority if needed
    # - Invoke the LLM with the technical-specific prompt to get a response
    # - Update the message status to "resolved"
    # - Add the message to history
    # - Add the LLM response to the messages list
    
    # Stub to make code runnable
    current_message = state["current_message"]
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    state["history"].append(current_message)
    state["messages"].append(AIMessage(content="This is a placeholder technical response."))
    return state

def handle_product_inquiry(state: AgentState) -> AgentState:
    """Handles product information inquiries."""
    # TODO:
    # - Extract the current message and content from the state
    # - Create a prompt for the product specialist
    # - Invoke the LLM with the product-specific prompt to get a response
    # - Update the message status to "resolved"
    # - Add the message to history
    # - Add the LLM response to the messages list
    
    # Stub to make code runnable
    current_message = state["current_message"]
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    state["history"].append(current_message)
    state["messages"].append(AIMessage(content="This is a placeholder product response."))
    return state

def handle_general_inquiry(state: AgentState) -> AgentState:
    """Handles general inquiries that don't fit other categories."""
    # TODO:
    # - Extract the current message and content from the state
    # - Create a prompt for the general customer service representative
    # - Invoke the LLM with the general inquiry prompt to get a response
    # - Update the message status to "resolved"
    # - Add the message to history
    # - Add the LLM response to the messages list
    
    # Stub to make code runnable
    current_message = state["current_message"]
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    state["history"].append(current_message)
    state["messages"].append(AIMessage(content="This is a placeholder general response."))
    return state

def route_message(state: AgentState) -> Dict[str, str]:
    """
    Determines which specialized handler should process the message
    based on the classification results.
    """
    # TODO:
    # - Extract message type and priority from the current message
    # - Create routing logic that:
    #   * Routes priority 1 messages to "priority_handling"
    #   * Routes other messages based on their type (billing, technical, product, general)
    # - Return a dictionary with the "next" key indicating the destination
    
    # Stub to make code runnable
    return {"next": "general"}

def handle_priority_inquiry(state: AgentState) -> AgentState:
    """Handles urgent inquiries with special priority treatment."""
    # TODO:
    # - Extract the current message, content, and message type from the state
    # - Create a specialized prompt for urgent cases that acknowledges urgency
    # - Invoke the LLM with the urgent inquiry prompt to get a detailed response
    # - Update the message status to "resolved_urgent"
    # - Add the message to history
    # - Add the LLM response to the messages list
    
    # Stub to make code runnable
    current_message = state["current_message"]
    current_message["status"] = "resolved_urgent"
    state["current_message"] = current_message
    state["history"].append(current_message)
    state["messages"].append(AIMessage(content="This is a placeholder urgent response."))
    return state

def create_customer_service_workflow():
    """Builds and returns the complete workflow graph."""
    # TODO:
    # - Initialize a StateGraph with AgentState
    # - Add nodes for classifier, router, and all handler functions
    # - Define the edges connecting the nodes:
    #   * Connect classifier to router
    #   * Add conditional edges from router to specialized handlers
    #   * Connect all handlers to END
    # - Set the entry point to the classifier
    # - Compile and return the workflow
    
    # Stub to make code runnable
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("classifier", classify_message)
    workflow.add_node("router", route_message)
    workflow.add_node("billing_handler", handle_billing_inquiry)
    workflow.add_node("technical_handler", handle_technical_inquiry)
    workflow.add_node("product_handler", handle_product_inquiry)
    workflow.add_node("general_handler", handle_general_inquiry)
    workflow.add_node("priority_handler", handle_priority_inquiry)
    
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
            "priority_handling": "priority_handler"
        }
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

def process_inquiry(message_content: str) -> Dict:
    """
    Processes a customer inquiry through the workflow.
    Returns the final state after processing.
    """
    # Initialize workflow
    workflow = create_customer_service_workflow()
    
    # Create initial state
    initial_state = AgentState(
        messages=[HumanMessage(content=message_content)],
        current_message={"content": message_content, "type": None, "priority": None, "status": "new"},
        history=[]
    )
    
    # Execute workflow
    result = workflow.invoke(initial_state)
    
    return result

# Example usage
if __name__ == "__main__":
    # Test with different inquiry types
    print("\n=== Testing with different inquiry types ===")
    
    # Billing inquiry
    print("\nProcessing as Billing Inquiry...")
    result = process_inquiry("I was charged twice for my subscription last month and need a refund.")
    print("\n=== BILLING INQUIRY ===")
    for message in result["messages"]:
        print(f"{type(message).__name__}: {message.content}")
    
    # Technical inquiry
    print("\nProcessing as Technical Inquiry...")
    result = process_inquiry("My account is locked and I can't reset my password. I've tried multiple times.")
    print("\n=== TECHNICAL INQUIRY ===")
    for message in result["messages"]:
        print(f"{type(message).__name__}: {message.content}")
    
    # Product inquiry
    print("\nProcessing as Product Inquiry...")
    result = process_inquiry("Does your premium plan include API access? I need details on rate limits.")
    print("\n=== PRODUCT INQUIRY ===")
    for message in result["messages"]:
        print(f"{type(message).__name__}: {message.content}")
    
    # Urgent inquiry
    print("\nProcessing as Urgent Inquiry...")
    result = process_inquiry("This is an emergency! My business account is showing $0 balance and all my client data is missing!")
    print("\n=== URGENT INQUIRY ===")
    for message in result["messages"]:
        print(f"{type(message).__name__}: {message.content}")

    print("\n==== End of Demo ====")