# Activity: Dynamic Message Routing with LangGraph

## Overview
In this hands-on coding activity, you'll build a dynamic message routing system using LangGraph. The system will intelligently process customer service inquiries by analyzing message content, determining inquiry priority, and routing messages through appropriate processing paths. You'll implement specialized nodes for different types of inquiries and create a flexible workflow that adapts based on message characteristics and system state.

## Learning Objectives
By completing this activity, you will be able to:
1. Implement a LangGraph workflow with conditional routing logic based on message classification
2. Design specialized processing nodes for different types of customer inquiries
3. Create a centralized routing mechanism using the hub-and-spoke pattern
4. Maintain conversation state across multiple interactions within a workflow
5. Implement priority-based processing to handle urgent inquiries appropriately

## Step-by-Step Instructions

### Step 1: Setup Environment and Import Dependencies
Ensure you have the necessary libraries installed. For this activity, you'll need langchain, langgraph, and access to an LLM API.

### Step 2: Define Message Structure and State
Create standardized message structures and the state management components needed for your workflow.

### Step 3: Implement Classification Node
Create a node responsible for analyzing incoming messages and determining their category and priority.

### Step 4: Develop Specialized Processing Nodes
Implement specialized nodes for different inquiry types (e.g., billing, technical support, product information).

### Step 5: Create Routing Logic
Build the conditional routing logic that will determine which processing path each message should follow.

### Step 6: Implement the Main Workflow Graph
Assemble all components into a complete LangGraph workflow with appropriate edges and conditions.

### Step 7: Test the System
Test your system with various types of customer inquiries to ensure proper routing and handling.

## Starter Code

```python
from typing import Annotated, List, Literal, TypedDict, Union, Dict, Optional
from langchain_core.messages import HumanMessage, AIMessage
import operator
from langchain_openai import ChatOpenAI
import json
from langgraph.graph import StateGraph, END

# You'll need to set your OpenAI API key
# import os
# os.environ["OPENAI_API_KEY"] = "your-api-key"

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

# Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# TODO: Implement the classifier node
def classify_message(state: AgentState) -> AgentState:
    """
    Analyzes the incoming message to determine its type and priority.
    Types can be: billing, technical, product, general
    Priority can be: 1 (urgent), 2 (high), 3 (medium), 4 (low)
    """
    # Your implementation here
    return state

# TODO: Implement specialized handling nodes
def handle_billing_inquiry(state: AgentState) -> AgentState:
    """Handles billing-related inquiries."""
    # Your implementation here
    return state

def handle_technical_inquiry(state: AgentState) -> AgentState:
    """Handles technical support inquiries."""
    # Your implementation here
    return state

def handle_product_inquiry(state: AgentState) -> AgentState:
    """Handles product information inquiries."""
    # Your implementation here
    return state

def handle_general_inquiry(state: AgentState) -> AgentState:
    """Handles general inquiries that don't fit other categories."""
    # Your implementation here
    return state

# TODO: Implement routing decision logic
def route_message(state: AgentState) -> Literal["billing", "technical", "product", "general"]:
    """
    Determines which specialized handler should process the message
    based on the classification results.
    """
    # Your implementation here
    return "general"  # Default routing

# TODO: Create the workflow graph
def create_customer_service_workflow():
    """Builds and returns the complete workflow graph."""
    # Your implementation here
    workflow = StateGraph(AgentState)
    
    # Add nodes
    
    # Add edges
    
    # Compile the graph
    
    return workflow

# Entry point function for testing
def process_inquiry(message_content: str) -> Dict:
    """
    Processes a customer inquiry through the workflow.
    Returns the final state after processing.
    """
    # Your implementation here
    return {"result": "Not implemented yet"}
```

## Solution Code

```python
from typing import Annotated, List, Literal, TypedDict, Union, Dict, Optional
from langchain_core.messages import HumanMessage, AIMessage
import operator
from langchain_openai import ChatOpenAI
import json
from langgraph.graph import StateGraph, END

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

# Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

def classify_message(state: AgentState) -> AgentState:
    """
    Analyzes the incoming message to determine its type and priority.
    Types can be: billing, technical, product, general
    Priority can be: 1 (urgent), 2 (high), 3 (medium), 4 (low)
    """
    current_message = state["current_message"]
    content = current_message["content"]
    
    # Create a prompt for the classifier
    classification_prompt = f"""
    Analyze the following customer service inquiry and classify it:
    
    Customer message: {content}
    
    Determine:
    1. Type (select one): billing, technical, product, general
    2. Priority (select one): 1 (urgent), 2 (high), 3 (medium), 4 (low)
    
    Respond with a JSON object with 'type' and 'priority' fields.
    """
    
    # Get classification from LLM
    response = llm.invoke(classification_prompt)
    
    try:
        # Extract JSON from the response
        classification = json.loads(response.content)
        
        # Update the current message with classification
        current_message["type"] = classification.get("type", "general")
        current_message["priority"] = classification.get("priority", 4)
        
        # Add a status field
        current_message["status"] = "classified"
        
        # Update the state
        state["current_message"] = current_message
        
        # Add the classification to messages
        state["messages"].append(
            AIMessage(content=f"Message classified as {current_message['type']} with priority {current_message['priority']}")
        )
        
    except json.JSONDecodeError:
        # Handle parsing errors by setting defaults
        current_message["type"] = "general"
        current_message["priority"] = 4
        current_message["status"] = "classification_failed"
        
        state["messages"].append(
            AIMessage(content="Failed to classify message. Treating as general inquiry.")
        )
    
    return state

def handle_billing_inquiry(state: AgentState) -> AgentState:
    """Handles billing-related inquiries."""
    current_message = state["current_message"]
    content = current_message["content"]
    priority = current_message["priority"]
    
    priority_note = ""
    if priority <= 2:
        priority_note = " This is a high-priority inquiry that requires immediate attention."
    
    response_prompt = f"""
    You are a billing specialist helping a customer with their inquiry.{priority_note}
    
    Customer inquiry: {content}
    
    Provide a helpful, professional response addressing their billing concern.
    """
    
    response = llm.invoke(response_prompt)
    
    # Update message status
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    
    # Add to history
    state["history"].append(current_message)
    
    # Add response to messages
    state["messages"].append(AIMessage(content=response.content))
    
    return state

def handle_technical_inquiry(state: AgentState) -> AgentState:
    """Handles technical support inquiries."""
    current_message = state["current_message"]
    content = current_message["content"]
    priority = current_message["priority"]
    
    priority_note = ""
    if priority <= 2:
        priority_note = " This is a high-priority technical issue that requires immediate attention."
    
    response_prompt = f"""
    You are a technical support specialist helping a customer with their issue.{priority_note}
    
    Customer inquiry: {content}
    
    Provide a helpful, professional response addressing their technical problem.
    Include troubleshooting steps when appropriate.
    """
    
    response = llm.invoke(response_prompt)
    
    # Update message status
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    
    # Add to history
    state["history"].append(current_message)
    
    # Add response to messages
    state["messages"].append(AIMessage(content=response.content))
    
    return state

def handle_product_inquiry(state: AgentState) -> AgentState:
    """Handles product information inquiries."""
    current_message = state["current_message"]
    content = current_message["content"]
    
    response_prompt = f"""
    You are a product information specialist helping a customer learn more about our products.
    
    Customer inquiry: {content}
    
    Provide a helpful, professional response with detailed product information.
    """
    
    response = llm.invoke(response_prompt)
    
    # Update message status
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    
    # Add to history
    state["history"].append(current_message)
    
    # Add response to messages
    state["messages"].append(AIMessage(content=response.content))
    
    return state

def handle_general_inquiry(state: AgentState) -> AgentState:
    """Handles general inquiries that don't fit other categories."""
    current_message = state["current_message"]
    content = current_message["content"]
    
    response_prompt = f"""
    You are a customer service representative handling a general inquiry.
    
    Customer inquiry: {content}
    
    Provide a helpful, professional response to their question or concern.
    """
    
    response = llm.invoke(response_prompt)
    
    # Update message status
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    
    # Add to history
    state["history"].append(current_message)
    
    # Add response to messages
    state["messages"].append(AIMessage(content=response.content))
    
    return state

def route_message(state: AgentState) -> Literal["billing", "technical", "product", "general", "priority_handling"]:
    """
    Determines which specialized handler should process the message
    based on the classification results.
    """
    message_type = state["current_message"]["type"]
    priority = state["current_message"]["priority"]
    
    # Special routing for very urgent inquiries
    if priority == 1:
        return "priority_handling"
    
    # Route based on message type
    if message_type == "billing":
        return "billing"
    elif message_type == "technical":
        return "technical"
    elif message_type == "product":
        return "product"
    else:
        return "general"

def handle_priority_inquiry(state: AgentState) -> AgentState:
    """Handles urgent inquiries with special priority treatment."""
    current_message = state["current_message"]
    content = current_message["content"]
    message_type = current_message["type"]
    
    # Prepare a special prompt for urgent cases
    response_prompt = f"""
    You are a senior customer service representative handling an URGENT inquiry.
    This requires immediate attention and priority handling.
    
    The inquiry is related to: {message_type}
    
    Customer inquiry: {content}
    
    Provide a detailed, reassuring response that acknowledges the urgency
    and offers a concrete next step or solution. Include information about
    expedited handling procedures for this priority case.
    """
    
    response = llm.invoke(response_prompt)
    
    # Update message status
    current_message["status"] = "resolved_urgent"
    state["current_message"] = current_message
    
    # Add to history
    state["history"].append(current_message)
    
    # Add response to messages
    state["messages"].append(AIMessage(content=response.content))
    
    return state

def create_customer_service_workflow():
    """Builds and returns the complete workflow graph."""
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
        lambda x: x["result"],
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
    
    # Billing inquiry
    result = process_inquiry("I was charged twice for my subscription last month and need a refund.")
    print("\n=== BILLING INQUIRY ===")
    for message in result["messages"]:
        print(f"{type(message).__name__}: {message.content}")
    
    # Technical inquiry
    result = process_inquiry("My account is locked and I can't reset my password. I've tried multiple times.")
    print("\n=== TECHNICAL INQUIRY ===")
    for message in result["messages"]:
        print(f"{type(message).__name__}: {message.content}")
    
    # Product inquiry
    result = process_inquiry("Does your premium plan include API access? I need details on rate limits.")
    print("\n=== PRODUCT INQUIRY ===")
    for message in result["messages"]:
        print(f"{type(message).__name__}: {message.content}")
    
    # Urgent inquiry
    result = process_inquiry("This is an emergency! My business account is showing $0 balance and all my client data is missing!")
    print("\n=== URGENT INQUIRY ===")
    for message in result["messages"]:
        print(f"{type(message).__name__}: {message.content}")
```

## Assessment Criteria

Your implementation will be assessed based on the following criteria:

1. **Functionality (40%)**
   - Does the system correctly classify and route messages to appropriate handlers?
   - Is priority-based routing implemented effectively?
   - Does the system maintain state correctly across the workflow?

2. **Code Quality (30%)**
   - Is the code well-organized and follow best practices?
   - Are functions clearly named and documented?
   - Is error handling implemented appropriately?

3. **LangGraph Implementation (20%)**
   - Proper use of LangGraph components (nodes, edges, conditions)
   - Effective graph structure design
   - Appropriate state management

4. **Testing and Documentation (10%)**
   - Comprehensive testing of different message types and priorities
   - Clear documentation of design decisions
   - Explanation of routing logic

## Extension Options

Here are some ways to extend this activity after completing the basic implementation:

1. **Multi-step Conversation Handling**
   - Implement a mechanism to handle follow-up questions within the same inquiry context
   - Create state transitions that can loop back to previous handlers

2. **Advanced Routing Logic**
   - Implement a more sophisticated routing algorithm that considers system load and agent availability
   - Create specialized paths for VIP customers or accounts with specific characteristics

3. **Performance Analytics**
   - Add instrumentation to track processing time at each node
   - Implement a dashboard that visualizes the flow of messages through the system

## Summary

This activity focuses on implementing dynamic message routing with LangGraph, a key component of building effective agent-based applications. You've created a system that intelligently processes customer service inquiries by analyzing content, determining priority, and routing through appropriate specialized handlers. This reinforces the hub-and-spoke architecture pattern and demonstrates how to implement conditional execution paths in LangGraph workflows.

Would you like me to clarify any part of this activity, or would you like suggestions for modifications to better fit your needs?