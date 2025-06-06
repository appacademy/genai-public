"""Utility nodes for the HR assistant orchestration graph."""

import time
from src.orchestration.utils import log_processing_time


def fallback(state, diagnostics, memory):
    """Generate a fallback response when no intent matches."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["fallback"],
    )

    # Generate the fallback response
    response = (
        "I'm sorry, I can only help with HR-related questions and tasks. "
        "I can assist with policies, benefits, or training - what would you like to know? "
        "Type 'help' to see what I can do."
    )

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Fallback", start_time)

    return {"response": response}
