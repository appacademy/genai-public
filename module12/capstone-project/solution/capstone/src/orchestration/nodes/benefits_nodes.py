"""Benefits-related nodes for the HR assistant orchestration graph."""

import time
from src.orchestration.utils import log_processing_time


def benefits_qa(state, benefits_rag, memory, diagnostics):
    """Generate a response to a benefits-related question."""
    start_time = time.time()

    # Store the current query for next time
    previous_question = state.user_input

    # Check if this is a follow-up question
    is_follow_up = state.previous_question and benefits_rag.is_followup_question(
        state.user_input, state.previous_question
    )

    # Get relevant history from memory
    relevant_history = (
        memory.get_relevant_history(
            state.user_input, topic=state.conversation_topic, count=3
        )
        if state.previous_question
        else []
    )

    # Log the query details
    diagnostics.log_query_processing(
        query=state.user_input,
        expanded_query=None,  # We'll update this after retrieval
        is_followup=is_follow_up,
        is_comparative=benefits_rag.is_comparative_question(state.user_input),
        is_sensitive=benefits_rag.is_sensitive_topic(state.user_input),
    )

    # Get context for the current query
    retrieval_start = time.time()
    context = benefits_rag.get_relevant_documents(state.user_input)
    retrieval_time = time.time() - retrieval_start

    # Log retrieval metrics
    diagnostics.log_context_retrieval(retrieval_time=retrieval_time, documents=context)

    # If this appears to be a follow-up question, include previous context
    combined_context = context
    if is_follow_up and state.previous_context:
        print(f"\nDetected follow-up question. Including previous context.\n")
        combined_context = state.previous_context + context

        # Also check if we should include context from relevant history
        if relevant_history:
            print(f"Including {len(relevant_history)} relevant previous interactions.")
            for hist_item in relevant_history:
                if "context_ids" in hist_item and hist_item.get("context", []):
                    combined_context.extend(hist_item.get("context", []))

    # Generate response with the appropriate context
    response = benefits_rag.generate_response(
        state.user_input,
        combined_context,
        previous_question=state.previous_question,
        previous_context=state.previous_context,
    )

    # Update memory with this interaction
    memory.update(state)

    # Generate memory diagnostics report if needed
    if is_follow_up:
        memory_report = memory.generate_diagnostics_report()
        print("\nMemory System Report:")
        print(memory_report)

    log_processing_time("Benefits QA", start_time)

    # Store current state as previous for next query
    return {
        "context": context,
        "response": response,
        "previous_question": previous_question,
        "previous_context": context,
        "previous_response": response,
    }
