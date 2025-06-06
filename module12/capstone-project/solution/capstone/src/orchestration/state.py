from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List


class GraphState(BaseModel):
    # Basic fields
    user_input: str = Field(description="The raw user input text")
    intent: Optional[Dict[str, Any]] = Field(None, description="The classified intent")
    context: Optional[List[Dict[str, Any]]] = Field(
        None, description="Retrieved context for RAG"
    )
    response: Optional[str] = Field(
        None, description="The final response to return to the user"
    )

    # Employee information
    employee_id: str = Field("current_user", description="The current employee ID")
    employee_name: Optional[str] = Field(None, description="The employee's name")
    is_new_employee: bool = Field(
        False, description="Whether the employee is new (< 7 days)"
    )
    department: Optional[str] = Field(None, description="The employee's department")
    role: Optional[str] = Field(None, description="The employee's role")

    # Conversation history
    previous_question: Optional[str] = Field(
        None, description="The previous user question"
    )
    previous_context: Optional[List[Dict[str, Any]]] = Field(
        None, description="Context from previous interactions"
    )
    previous_response: Optional[str] = Field(None, description="The previous response")
    conversation_topic: Optional[str] = Field(
        None, description="The current conversation topic"
    )
