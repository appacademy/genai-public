from typing import Dict
from models.state import AgentState


def route_message(state: AgentState) -> Dict[str, str]:
    """
    Determines which specialized handler should process the message
    based on the classification results.
    """
    # TODO: Implement the routing logic that:
    # - Routes priority 1 messages to priority_handling
    # - Routes other messages based on their type (billing, technical, product, general)
    # - Returns a dictionary with the "next" key set to the appropriate handler name

    # TODO: Extract message type and priority from the current message

    # TODO: Implement priority-based routing for urgent messages

    # TODO: Implement type-based routing for non-urgent messages

    return {"next": "general"}  # Default routing
