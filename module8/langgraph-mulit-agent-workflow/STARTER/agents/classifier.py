import json
import re
from models.state import AgentState
from langchain_core.messages import AIMessage


def extract_json_from_text(text):
    """Extract JSON from text that might contain markdown or explanatory content."""
    # TODO: Try direct JSON parsing first

    # TODO: Look for JSON in code blocks

    # TODO: Look for JSON-like patterns

    # TODO: Extract individual fields as fallback

    # TODO: Return None if no JSON found


def classify_message(state: AgentState, ollama_client) -> AgentState:
    """
    Analyzes the incoming message to determine its type and priority.
    Types can be: billing, technical, product, general
    Priority can be: 1 (urgent), 2 (high), 3 (medium), 4 (low)
    """
    # TODO: 1. Extract the content from the current message in the state

    # TODO: 2. Create a classification prompt that asks the LLM to determine:
    #    - Type (billing, technical, product, general)
    #    - Priority (1-urgent, 2-high, 3-medium, 4-low)

    # TODO: 3. Request a response from the ollama_client using the prompt

    # TODO: 4. Extract the classification JSON from the response using extract_json_from_text()

    # TODO: 5. Update the current message with the type and priority

    # TODO: 6. Set the message status to "classified"

    # TODO: 7. Add a classification notification to the messages list

    # TODO: 8. Handle any parsing errors by setting default values

    # TODO: Return the updated state
