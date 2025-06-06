"""Node function definitions for the HR assistant orchestration graph."""

from src.orchestration.nodes.classification_nodes import classify_intent
from src.orchestration.nodes.policy_nodes import policy_qa
from src.orchestration.nodes.benefits_nodes import benefits_qa
from src.orchestration.nodes.training_nodes import (
    training_lookup,
    training_courses,
    training_enroll,
    training_update,
    mandatory_training,
)
from src.orchestration.nodes.hr_nodes import (
    hr_employees,
    hr_training,
    hr_employee_training,
    hr_bulk_add_employees,
    hr_update_employee,
    hr_analytics,
)
from src.orchestration.nodes.utility_nodes import fallback

__all__ = [
    "classify_intent",
    "policy_qa",
    "benefits_qa",
    "training_lookup",
    "training_courses",
    "training_enroll",
    "training_update",
    "mandatory_training",
    "hr_employees",
    "hr_training",
    "hr_employee_training",
    "hr_bulk_add_employees",
    "hr_update_employee",
    "hr_analytics",
    "fallback",
]
