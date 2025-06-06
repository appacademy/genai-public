"""Classification nodes for the HR assistant orchestration graph."""

import time
from src.orchestration.utils import classify_topic, log_processing_time


def classify_intent(state, intent_router, diagnostics):
    """Classify the intent of the user query."""
    start_time = time.time()

    # Classify the intent
    intent_data = intent_router.classify(state.user_input)

    # Determine conversation topic
    conversation_topic = classify_topic(state.user_input, intent_data)

    # Log query processing information
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=(state.previous_question is not None),
        detected_entities=intent_data.get("entities", []),
    )

    log_processing_time("Intent classification", start_time)

    return {"intent": intent_data, "conversation_topic": conversation_topic}
