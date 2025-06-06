"""Utility functions for orchestration."""

import time


def classify_topic(query, intent):
    """Classify the topic of conversation based on query and intent."""
    topic_keywords = {
        "pto": "leave_policy",
        "vacation": "leave_policy",
        "time off": "leave_policy",
        "sick leave": "leave_policy",
        "maternity": "leave_policy",
        "paternity": "leave_policy",
        "bereavement": "leave_policy",
        "health": "benefits",
        "insurance": "benefits",
        "medical": "benefits",
        "dental": "benefits",
        "vision": "benefits",
        "401k": "benefits",
        "retirement": "benefits",
        "harassment": "workplace_policy",
        "discrimination": "workplace_policy",
        "code of conduct": "workplace_policy",
        "dress code": "workplace_policy",
        "remote work": "workplace_policy",
        "work from home": "workplace_policy",
        "training": "training",
        "course": "training",
        "certification": "training",
    }

    query_lower = query.lower()

    # First check if intent already tells us the topic
    if intent and "intent" in intent:
        if intent["intent"] == "policy_q":
            # Try to determine which specific policy
            for keyword, topic in topic_keywords.items():
                if keyword in query_lower:
                    return topic
            return "general_policy"
        elif intent["intent"] == "benefit_q":
            return "benefits"
        elif intent["intent"].startswith("train_"):
            return "training"

    # Otherwise check query text
    for keyword, topic in topic_keywords.items():
        if keyword in query_lower:
            return topic

    return "general"


def log_processing_time(func_name, start_time):
    """Log the processing time of a function."""
    total_time = time.time() - start_time
    print(f"{func_name} completed in {total_time:.3f}s")
