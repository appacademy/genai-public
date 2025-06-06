from models.state import AgentState
from langchain_core.messages import AIMessage


def handle_priority_inquiry(
    state: AgentState, ollama_client, knowledge_base
) -> AgentState:
    """Handles urgent inquiries with special priority treatment."""
    current_message = state["current_message"]
    content = current_message["content"]
    message_type = current_message["type"]
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

    # Get context for priority inquiries and the specific domain
    priority_context = knowledge_base.get_context_for_prompt("priority")
    domain_context = knowledge_base.get_context_for_prompt(message_type)

    # Prepare a special prompt for urgent cases
    response_prompt = f"""
    You are a senior customer service representative handling an URGENT inquiry.
    This requires immediate attention and priority handling.
    
    The inquiry is related to: {message_type}
    
    PRIORITY HANDLING CONTEXT:
    {priority_context}
    
    DOMAIN-SPECIFIC CONTEXT:
    {domain_context}
    
    Customer inquiry: {content}
    {f"Additional context: {additional_context}" if additional_context else ""}
    
    Provide a detailed, reassuring response that acknowledges the urgency
    and offers a concrete next step or solution. Include information about
    expedited handling procedures for this priority case.
    Reference specific emergency procedures and escalation paths when applicable.
    
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
    current_message["status"] = "resolved_urgent"
    state["current_message"] = current_message

    # Add to history
    state["history"].append(current_message)

    # Add response to messages
    state["messages"].append(AIMessage(content=response_str))

    return state
