"""Graph-based orchestration for the HR assistant."""

from langgraph.graph import StateGraph, END
import time
import pandas as pd
from src.orchestration.memory import ConversationMemory, ConversationDiagnostics
from src.orchestration.state import GraphState
from src.orchestration.nodes import (
    classify_intent,
    policy_qa,
    benefits_qa,
    training_lookup,
    training_courses,
    training_enroll,
    training_update,
    mandatory_training,
    hr_employees,
    hr_training,
    hr_employee_training,
    hr_bulk_add_employees,
    hr_update_employee,
    hr_analytics,
    fallback,
)


def create_workflow(intent_router, policy_rag, benefits_rag, training_records, llm):
    """Create the LangGraph workflow for orchestrating the HR assistant."""
    workflow = StateGraph(GraphState)

    # Initialize conversation memory and diagnostics
    memory = ConversationMemory()
    diagnostics = ConversationDiagnostics()

    # Define node wrappers that inject dependencies
    def classify_intent_node(state):
        return classify_intent(state, intent_router, diagnostics)

    def policy_qa_node(state):
        return policy_qa(state, policy_rag, memory, diagnostics)

    def benefits_qa_node(state):
        return benefits_qa(state, benefits_rag, memory, diagnostics)

    def training_lookup_node(state):
        return training_lookup(state, training_records, diagnostics, memory)

    def training_courses_node(state):
        return training_courses(state, training_records, diagnostics, memory)

    def training_enroll_node(state):
        return training_enroll(state, training_records, diagnostics, memory)

    def training_update_node(state):
        return training_update(state, training_records, diagnostics, memory)

    def mandatory_training_node(state):
        return mandatory_training(state, training_records, diagnostics, memory)

    def hr_employees_node(state):
        return hr_employees(state, diagnostics, memory)

    def hr_training_node(state):
        return hr_training(state, diagnostics, memory)

    def hr_employee_training_node(state):
        return hr_employee_training(state, diagnostics, memory)

    def hr_bulk_add_employees_node(state):
        return hr_bulk_add_employees(state, diagnostics, memory, training_records)

    def hr_update_employee_node(state):
        return hr_update_employee(state, diagnostics, memory)

    def hr_analytics_node(state):
        return hr_analytics(state, diagnostics, memory)

    def fallback_node(state):
        return fallback(state, diagnostics, memory)

    # Add nodes to graph
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("policy_qa", policy_qa_node)
    workflow.add_node("benefits_qa", benefits_qa_node)
    workflow.add_node("training_lookup", training_lookup_node)
    workflow.add_node("training_courses", training_courses_node)
    workflow.add_node("training_enroll", training_enroll_node)
    workflow.add_node("training_update", training_update_node)
    workflow.add_node("mandatory_training", mandatory_training_node)
    workflow.add_node("hr_employees", hr_employees_node)
    workflow.add_node("hr_training", hr_training_node)
    workflow.add_node("hr_employee_training", hr_employee_training_node)
    workflow.add_node("hr_bulk_add", hr_bulk_add_employees_node)
    workflow.add_node("hr_update", hr_update_employee_node)
    workflow.add_node("hr_analytics", hr_analytics_node)
    workflow.add_node("fallback", fallback_node)

    # Define edges
    workflow.set_entry_point("classify_intent")

    # Route based on intent
    workflow.add_conditional_edges(
        "classify_intent",
        lambda state: state.intent["intent"],
        {
            "policy_q": "policy_qa",
            "benefit_q": "benefits_qa",
            "train_lookup": "training_lookup",
            "train_courses": "training_courses",
            "train_enroll": "training_enroll",
            "train_update": "training_update",
            "train_mandatory": "mandatory_training",
            "hr_employees": "hr_employees",
            "hr_training": "hr_training",
            "hr_employee_training": "hr_employee_training",
            "hr_bulk_add": "hr_bulk_add",
            "hr_update": "hr_update",
            "hr_analytics": "hr_analytics",
            "fallback": "fallback",
        },
    )

    # All nodes except classify_intent are terminal
    workflow.add_edge("policy_qa", END)
    workflow.add_edge("benefits_qa", END)
    workflow.add_edge("training_lookup", END)
    workflow.add_edge("training_courses", END)
    workflow.add_edge("training_enroll", END)
    workflow.add_edge("training_update", END)
    workflow.add_edge("mandatory_training", END)
    workflow.add_edge("hr_employees", END)
    workflow.add_edge("hr_training", END)
    workflow.add_edge("hr_employee_training", END)
    workflow.add_edge("hr_bulk_add", END)
    workflow.add_edge("hr_update", END)
    workflow.add_edge("hr_analytics", END)
    workflow.add_edge("fallback", END)

    return workflow.compile()
