from typing import List, Literal, TypedDict, Union, Dict, Optional
from langchain_core.messages import HumanMessage, AIMessage


# Define our message types and state
class Message(TypedDict):
    content: str
    type: Optional[str]
    priority: Optional[int]
    status: Optional[str]
    user_name: Optional[str]
    user_email: Optional[str]
    additional_context: Optional[str]


class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]
    current_message: Message
    history: List[Message]
