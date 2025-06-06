import json
import re
from models.state import AgentState
from langchain_core.messages import AIMessage


def extract_json_from_text(text):
    """Extract JSON from text that might contain markdown or explanatory content."""
    # Try direct JSON parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Look for JSON in code blocks
    code_block_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    code_blocks = re.findall(code_block_pattern, text)
    if code_blocks:
        for block in code_blocks:
            try:
                return json.loads(block)
            except json.JSONDecodeError:
                continue

    # Look for JSON-like patterns
    json_pattern = r"\{[^}]*\"type\"[^}]*\"priority\"[^}]*\}"
    json_matches = re.findall(json_pattern, text)
    if json_matches:
        for match in json_matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue

    # If all else fails, try to construct JSON from the text
    type_match = re.search(r"type[\"']?\s*:\s*[\"'](\w+)[\"']", text, re.IGNORECASE)
    priority_match = re.search(r"priority[\"']?\s*:\s*(\d+)", text, re.IGNORECASE)

    if type_match or priority_match:
        result = {}
        if type_match:
            result["type"] = type_match.group(1).lower()
        if priority_match:
            result["priority"] = int(priority_match.group(1))
        return result

    return None


def classify_message(state: AgentState, ollama_client) -> AgentState:
    """
    Analyzes the incoming message to determine its type and priority.
    Types can be: billing, technical, product, general
    Priority can be: 1 (urgent), 2 (high), 3 (medium), 4 (low)
    """
    current_message = state["current_message"]
    content = current_message["content"]

    # Create a prompt for the classifier
    classification_prompt = f"""
    Analyze the following customer service inquiry and classify it:
    
    Customer message: {content}
    
    Determine:
    1. Type (select one): billing, technical, product, general
    2. Priority (select one): 1 (urgent), 2 (high), 3 (medium), 4 (low)
    
    Respond with a JSON object with 'type' and 'priority' fields.
    Format your response as a valid JSON object like this example:
    {{
      "type": "billing",
      "priority": 2
    }}
    
    Do not include any explanations or additional text, just the JSON object.
    """

    # Get classification from LLM
    ollama_response = ollama_client.generate(classification_prompt)
    response_str = ollama_response["response"]

    # Try to extract JSON from the response
    classification = extract_json_from_text(response_str)

    if classification and "type" in classification:
        # Update the current message with classification
        current_message["type"] = classification.get("type", "general")
        current_message["priority"] = classification.get("priority", 4)

        # Add a status field
        current_message["status"] = "classified"

        # Update the state
        state["current_message"] = current_message

        # Add the classification to messages
        state["messages"].append(
            AIMessage(
                content=f"Message classified as {current_message['type']} with priority {current_message['priority']}"
            )
        )
    else:
        # Handle parsing errors by setting defaults
        current_message["type"] = "general"
        current_message["priority"] = 4
        current_message["status"] = "classification_failed"

        state["messages"].append(
            AIMessage(
                content="Failed to classify message. Treating as general inquiry."
            )
        )

    return state
