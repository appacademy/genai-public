from typing import Dict
from models.state import AgentState


def route_message(state: AgentState) -> Dict[str, str]:
    """
    Determines which specialized handler should process the message
    based on the classification results.
    """
    message_type = state["current_message"]["type"]
    priority = state["current_message"]["priority"]

    # Special routing for very urgent inquiries
    if priority == 1:
        return {"next": "priority_handling"}

    # Route based on message type
    if message_type == "billing":
        return {"next": "billing"}
    elif message_type == "technical":
        return {"next": "technical"}
    elif message_type == "product":
        return {"next": "product"}
    else:
        return {"next": "general"}
