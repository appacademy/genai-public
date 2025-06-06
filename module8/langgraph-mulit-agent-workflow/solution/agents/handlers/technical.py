from models.state import AgentState
from langchain_core.messages import AIMessage


def handle_technical_inquiry(
    state: AgentState, ollama_client, knowledge_base
) -> AgentState:
    """Handles technical support inquiries."""
    current_message = state["current_message"]
    content = current_message["content"]
    priority = current_message["priority"]
    user_name = current_message.get("user_name")
    additional_context = current_message.get("additional_context")

    # Personalized greeting if name is provided
    greeting = f"Hello {user_name}, " if user_name else ""

    # Context acknowledgment if provided
    context_acknowledgment = ""
    if additional_context:
        context_acknowledgment = (
            f"Based on the additional context you provided ({additional_context}), "
        )

    # Get context for technical inquiries
    technical_context = knowledge_base.get_context_for_prompt("technical")

    priority_note = ""
    if priority <= 2:
        priority_note = " This is a high-priority technical issue that requires immediate attention."

    response_prompt = f"""
    You are a technical support specialist helping a customer with their issue.{priority_note}
    
    IMPORTANT CONTEXT:
    {technical_context}
    
    Customer inquiry: {content}
    {f"Additional context: {additional_context}" if additional_context else ""}
    
    Provide a helpful, professional response addressing their technical problem.
    Include troubleshooting steps when appropriate.
    Reference specific company policies and procedures when applicable.
    
    IMPORTANT: Sign your response with the following format:
    
    Emma G.
    AI Customer Support Representative
    SaaS Solutions Inc.
    {f"Start with a personalized greeting: '{greeting}'" if user_name else ""}
    {f"Acknowledge the additional context: '{context_acknowledgment}'" if additional_context else ""}
    """

    ollama_response = ollama_client.generate(response_prompt)
    response_str = ollama_response["response"]

    # Ensure the response has Emma's signature if it's missing
    if "Emma G." not in response_str:
        response_str += (
            "\n\nEmma G.\nAI Customer Support Representative\nSaaS Solutions Inc."
        )

    # Update message status
    current_message["status"] = "resolved"
    state["current_message"] = current_message

    # Add to history
    state["history"].append(current_message)

    # Add response to messages
    state["messages"].append(AIMessage(content=response_str))

    return state
