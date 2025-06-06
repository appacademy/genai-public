# Activity: Implementing a Multi-Agent Workflow with LangGraph



## Overview

In this hands-on coding activity, we'll build a customer service multi-agent system using LangGraph. The system will intelligently process customer inquiries by classifying message content, determining priority levels, and routing messages to specialized handling agents. we'll create a flexible workflow that adapts to different inquiry types and uses a knowledge base to provide personalized, contextually relevant responses. This project demonstrates how to implement a production-ready agent architecture that maintains conversation state and handles different inquiry scenarios effectively.



## Learning Objectives

By completing this activity, you will be able to:
1. Implement a LangGraph workflow with conditional routing logic based on message classification
2. Design specialized processing nodes for different types of customer inquiries
3. Create a centralized routing mechanism using the hub-and-spoke pattern
4. Maintain conversation state across multiple interactions within a workflow
5. Implement priority-based processing to handle urgent inquiries appropriately



## Time Estimate

120 minutes



## Prerequisites

- Python 3.12
- Basic understanding of LangGraph components and workflows
- Familiarity with Python libraries and package installation
- Ollama installed locally with the Gemma3:4b model
- A code editor (VS Code recommended)



## Setup Instructions

### Step 1: Clone the Repository

Clone the starter code repository to your local machine:

```bash
git clone https://github.com/[organization]/customer-service-workflow-starter.git
cd customer-service-workflow-starter
```



### Step 2: Create and Activate a Virtual Environment

Create and then activate a virtual environment for your project using the commands for your system:

- **Mac/Linux**:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- **Windows (PowerShell)**:

  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  ```

- **Windows (Git Bash)**:

  ```bash
  python -m venv .venv
  source .venv/Scripts/activate
  ```

After activation, your terminal prompt should change (e.g., `(venv)` appears).



### Step 3: Install Dependencies

With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

The requirements.txt file contains the following dependencies:

```
langchain-core==0.3.48
langgraph==0.3.21
requests==2.32.3
python-dotenv==1.0.1
```



### Step 4: Configure Environment

1. Create a `.env` file from the template:

   ```bash
   # Mac/Linux
   cp .env.template .env
   
   # Windows (PowerShell/Command Prompt)
   copy .env.template .env
   ```

2. The default configuration uses Ollama at `http://localhost:11434`. If you're using a different URL, update the `OLLAMA_API_URL` in the `.env` file.



### Step 5: Start Ollama

1. Ensure Ollama is installed on your system. If not, download it from [ollama.ai](https://ollama.ai).

2. Start Ollama with the Gemma3:4b model:

   ```bash
   # All operating systems
   ollama run gemma3:4b
   ```

   This will download the model if it's not already on your system and start the Ollama service.



## Key Concepts

### Multi-Agent Architecture

The customer service workflow system uses a multi-agent architecture with several key components:

1. **Classifier Agent**: Analyzes incoming customer inquiries to determine their type (billing, technical, product, general) and priority level (1-4)

2. **Router**: Routes classified messages to specialized handling agents based on message type and priority

3. **Specialized Handlers**: Domain-specific agents that generate appropriate responses:
   - Billing handler (for subscription and payment issues)
   - Technical handler (for technical support questions)
   - Product handler (for product information inquiries)
   - General handler (for miscellaneous inquiries)
   - Priority handler (for urgent issues requiring immediate attention)

4. **Knowledge Base**: Provides context-specific information to each specialized handler to inform their responses

### LangGraph Workflow Management

The system uses LangGraph to create a directed graph that orchestrates the flow of information:

1. **Nodes**: Each agent or processing step is represented as a node in the graph
2. **Edges**: Define the possible transitions between nodes
3. **Conditional Routing**: Messages follow different paths through the graph based on their classification
4. **State Management**: The workflow maintains consistent state as messages progress through the system

### Inquiry Classification and Routing

The system uses a two-step process for handling inquiries:

1. **Classification**: Analyzes the message content to determine:
   - Type (billing, technical, product, general)
   - Priority (1-urgent, 2-high, 3-medium, 4-low)

2. **Routing**: Directs the message to the appropriate handler based on:
   - Message type for standard routing
   - Priority-based routing for urgent messages

### Response Generation and Personalization

The system generates personalized responses through:

1. **Knowledge Base Integration**: Each handler has access to domain-specific knowledge
2. **Priority Recognition**: Acknowledges urgent issues with appropriate escalation
3. **User Information Integration**: Personalizes responses with user name and context
4. **Consistent Identity**: Maintains a consistent AI identity (Emma G.) across all responses



## LangGraph Framework

This activity uses the LangGraph framework to orchestrate the workflow. LangGraph is built on top of LangChain and provides powerful tools for creating directed graphs of components that can be connected together to form complex workflows.

For a practical introduction to LangGraph implementation specific to this activity, see the [LangGraph Implementation Guide](resources/langgraph_implementation_guide.md).

Key LangGraph components used in this activity:

1. **StateGraph**: The primary construct for defining a workflow with state management
2. **Nodes**: Individual processing components that transform state
3. **Edges**: Connections between nodes that define valid transitions
4. **Conditional Edges**: Routes that depend on the outcome of a previous node
5. **State Management**: Mechanism for passing information between nodes

The workflow diagram shows how different components connect:

```
                     ┌─────────────┐
                     │             │
                     │ Classifier  │
                     │             │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │             │
                     │   Router    │
                     │             │
                     └──────┬──────┘
                            │
           ┌────────┬───────┼───────┬────────┐
           │        │       │       │        │
           ▼        ▼       ▼       ▼        ▼
┌─────────────┐ ┌─────────┐ ┌─────┐ ┌─────┐ ┌─────────────┐
│             │ │         │ │     │ │     │ │             │
│  Priority   │ │ Billing │ │Tech │ │Prod │ │   General   │
│   Handler   │ │ Handler │ │Hand │ │Hand │ │   Handler   │
│             │ │         │ │     │ │     │ │             │
└─────────────┘ └─────────┘ └─────┘ └─────┘ └─────────────┘
           │        │       │       │        │
           │        │       │       │        │
           └────────┴───────┼───────┴────────┘
                            │
                            ▼
                          END
```



## Activity Tasks

In this activity, we'll implement several key components of the Customer Service Multi-Agent Workflow system by completing the TODO items in the starter code. Each task focuses on an important aspect of building a LangGraph-based workflow for intelligent customer service automation.

### Task 1: Implement Message Classification

1. Our first task is to implement the message classification functionality in the `agents/classifier.py` file. we'll need to complete the `classify_message` function that analyzes incoming customer inquiries to determine their type and priority level. This task demonstrates effective prompt engineering and robust error handling when working with LLM outputs.

    **Step 1.1**. Find the TODO comment: "1. Extract the content from the current message in the state" and add this code snippet:
    
    ```python
    current_message = state["current_message"]
    content = current_message["content"]
    ```
    
    This code retrieves the current message from the state object and extracts its content for classification.
    
    **Step 1.2**. Find the TODO comment: "2. Create a classification prompt that asks the LLM to determine:" and add this code snippet:
    
    ```python
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
    ```
    
    This code creates a detailed prompt that instructs the LLM to analyze the customer message and classify it by type and priority, requesting the response in JSON format.
    
    **Step 1.3**. Find the TODO comment: "3. Request a response from the ollama_client using the prompt" and add this code snippet:
    
    ```python
    # Get classification from LLM
    ollama_response = ollama_client.generate(classification_prompt)
    response_str = ollama_response["response"]
    ```
    
    This code sends the classification prompt to the Ollama LLM client and extracts the text response from the returned object.
    
    **Step 1.4**. Find the TODO comment: "4. Extract the classification JSON from the response using extract_json_from_text()" and add this code snippet:
    
    ```python
    # Try to extract JSON from the response
    classification = extract_json_from_text(response_str)
    ```
    
    This code uses the provided helper function to parse the JSON classification data from the LLM's response, handling various response formats.
    
    **Step 1.5**. Find the TODO comment: "5. Update the current message with the type and priority" and "6. Set the message status to 'classified'" and "7. Add a classification notification to the messages list" and add this code snippet:
    
    ```python
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
    ```
    
    This code updates the current message with the classification results, sets its status to "classified", and adds a notification to the conversation history showing the classification results.
    
    **Step 1.6**. Find the TODO comment: "8. Handle any parsing errors by setting default values" and add this code snippet:
    
    ```python
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
    ```
    
    This code implements error handling for cases where classification fails, setting reasonable defaults (general type, priority 4) and adding a notification about the failure to the conversation history.
    
    **Step 1.7**. Find the TODO comment: "Return the updated state" and add this code snippet:
    
    ```python
    return state
    ```
    
    This code returns the updated state object with the classified message and notification.


2. Implement the `extract_json_from_text` function.

    **Step 1.8**. Find the TODO comment: "Try direct JSON parsing first" and add this code snippet:
    
    ```python
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    ```
    
    This code attempts to parse the input text directly as JSON. If successful, it returns the parsed JSON object. If the text is not valid JSON, it catches the exception and continues to the next method.
    
    **Step 1.9**. Find the TODO comment: "Look for JSON in code blocks" and add this code snippet:
    
    ```python
    code_block_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    code_blocks = re.findall(code_block_pattern, text)
    if code_blocks:
        for block in code_blocks:
            try:
                return json.loads(block)
            except json.JSONDecodeError:
                continue
    ```
    
    This code searches for content inside markdown code blocks (```json...```) using regular expressions. It tries to parse each code block as JSON and returns the first valid JSON object found.
    
    **Step 1.10**. Find the TODO comment: "Look for JSON-like patterns" and add this code snippet:
    
    ```python
    json_pattern = r"\{[^}]*\"type\"[^}]*\"priority\"[^}]*\}"
    json_matches = re.findall(json_pattern, text)
    if json_matches:
        for match in json_matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
    ```
    
    This code uses a regular expression to find text that looks like JSON containing both "type" and "priority" fields. It attempts to parse each match as JSON and returns the first valid result.
    
    **Step 1.11**. Find the TODO comment: "Extract individual fields as fallback" and add this code snippet:
    
    ```python
    type_match = re.search(r"type[\"']?\s*:\s*[\"'](\w+)[\"']", text, re.IGNORECASE)
    priority_match = re.search(r"priority[\"']?\s*:\s*(\d+)", text, re.IGNORECASE)

    if type_match or priority_match:
        result = {}
        if type_match:
            result["type"] = type_match.group(1).lower()
        if priority_match:
            result["priority"] = int(priority_match.group(1))
        return result
    ```
    
    This code is a fallback method that searches for individual "type" and "priority" fields using regular expressions. If either field is found, it constructs a JSON object with the extracted values.
    
    **Step 1.12**. Find the TODO comment: "Return None if no JSON found" and add this code snippet:
    
    ```python
    return None
    ```
    
    This code returns None if all previous methods fail to extract JSON from the text, indicating that no valid JSON could be found.


### Task 2: Implement Routing Logic

1. For Task 2, we'll implement the routing mechanism in the `agents/router.py` file by implementing the `route_message` function. 
   
   This function serves as the central hub in the workflow's hub-and-spoke architecture, determining which specialized handler should process each customer inquiry. This task demonstrates implementing conditional routing logic in a LangGraph workflow, allowing the system to adapt its behavior based on message characteristics.

    **Step 2.1**. Find the TODO comment: "Implement the routing logic that:" and follow the steps below.
    
    **Step 2.2**. Find the TODO comment: "Extract message type and priority from the current message" and add this code snippet:
    
    ```python
    message_type = state["current_message"]["type"]
    priority = state["current_message"]["priority"]
    ```
    
    This code extracts both the message type and priority from the current message stored in the state.
    
    **Step 2.3**. Find the TODO comment: "Implement priority-based routing for urgent messages" and add this code snippet:
    
    ```python
    # Special routing for very urgent inquiries
    if priority == 1:
        return {"next": "priority_handling"}
    ```
    
    This code checks if the message has priority level 1 (urgent). If so, it routes the message directly to the priority handler, regardless of message type.
    
    **Step 2.4**. Find the TODO comment: "Implement type-based routing for non-urgent messages" and add this code snippet:
    
    ```python
    # Route based on message type
    if message_type == "billing":
        return {"next": "billing"}
    elif message_type == "technical":
        return {"next": "technical"}
    elif message_type == "product":
        return {"next": "product"}
    else:
        return {"next": "general"}
    ```
    
    This code routes non-urgent messages based on their type. Billing inquiries go to the billing handler, technical inquiries to the technical handler, product inquiries to the product handler, and all other types to the general handler.

---
### Task 3: Implement Specialized Handlers

1. In this task, we'll implement specialized response handlers for different inquiry types in the `agents/handlers/` directory. Start with the billing handler in `billing.py` by implementing the `handle_billing_inquiry` function. 

    **Step 3.1**. Find the TODO comment: "1. Extract message details (content, priority, user info) from state" and add this code snippet:
    
    ```python
    current_message = state["current_message"]
    content = current_message["content"]
    priority = current_message["priority"]
    user_name = current_message.get("user_name")
    additional_context = current_message.get("additional_context")
    ```
    
    This code extracts all relevant details from the current message, including the content, priority level, user name (if available), and any additional context information.
    
    **Step 3.2**. Find the TODO comment: "2. Create personalized greeting if user name is provided" and add this code snippet:
    
    ```python
    # Personalized greeting if name is provided
    greeting = f"Hello {user_name}, " if user_name else ""

    # Context acknowledgment if provided
    context_acknowledgment = ""
    if additional_context:
        context_acknowledgment = (
            f"Based on the additional context you provided ({additional_context}), "
        )
    ```
    
    This code creates a personalized greeting when a user name is available and acknowledges any additional context information that was provided with the inquiry.
    
    **Step 3.3**. Find the TODO comment: "3. Get billing-specific context from the knowledge base" and add this code snippet:
    
    ```python
    # Get context for billing inquiries
    billing_context = knowledge_base.get_context_for_prompt("billing")
    ```
    
    This code retrieves domain-specific knowledge about billing from the knowledge base to provide accurate information in the response.
    
    **Step 3.4**. Find the TODO comment: "4. Add priority note for high-priority inquiries" and add this code snippet:
    
    ```python
    priority_note = ""
    if priority <= 2:
        priority_note = (
            " This is a high-priority inquiry that requires immediate attention."
        )
    ```
    
    This code adds a special note for high-priority inquiries (priority levels 1-2) to ensure they receive appropriate attention.
    
    **Step 3.5**. Find the TODO comment: "5. Create a detailed prompt including:" and add this code snippet:
    
    ```python
    response_prompt = f"""
    You are a billing specialist helping a customer with their inquiry.{priority_note}
    
    IMPORTANT CONTEXT:
    {billing_context}
    
    Customer inquiry: {content}
    {f"Additional context: {additional_context}" if additional_context else ""}
    
    Provide a helpful, professional response addressing their billing concern.
    Reference specific company policies when applicable.
    
    IMPORTANT: Sign your response with the following format:
    
    Emma G.
    AI Customer Support Representative
    SaaS Solutions Inc.
    {f"Start with a personalized greeting: '{greeting}'" if user_name else ""}
    {f"Acknowledge the additional context: '{context_acknowledgment}'" if additional_context else ""}
    """
    ```
    
    This code constructs a comprehensive prompt that includes the knowledge base context, customer inquiry, personalization elements, and detailed instructions for the LLM to generate an appropriate response.
    
    **Step 3.6**. Find the TODO comment: "6. Generate a response using ollama_client" and add this code snippet:
    
    ```python
    ollama_response = ollama_client.generate(response_prompt)
    response_str = ollama_response["response"]
    ```
    
    This code sends the prompt to the Ollama client and retrieves the generated response.
    
    **Step 3.7**. Find the TODO comment: "7. Ensure the response includes Emma G.'s signature" and add this code snippet:
    
    ```python
    # Ensure the response has Emma's signature if it's missing
    if "Emma G." not in response_str:
        response_str += (
            "\n\nEmma G.\nAI Customer Support Representative\nSaaS Solutions Inc."
        )
    ```
    
    This code checks if the response includes Emma G.'s signature and adds it if it's missing, ensuring brand consistency.
    
    **Step 3.8**. Find the TODO comment: "8. Update message status to 'resolved'" and add this code snippet:
    
    ```python
    # Update message status
    current_message["status"] = "resolved"
    state["current_message"] = current_message
    ```
    
    This code updates the message status to "resolved" to indicate that the inquiry has been addressed.
    
    **Step 3.9**. Find the TODO comment: "9. Add the message to history" and add this code snippet:
    
    ```python
    # Add to history
    state["history"].append(current_message)
    ```
    
    This code adds the current message to the conversation history for record-keeping.
    
    **Step 3.10**. Find the TODO comment: "10. Add the AI response to messages" and add this code snippet:
    
    ```python
    # Add response to messages
    state["messages"].append(AIMessage(content=response_str))
    
    return state
    ```
    
    This code adds the AI-generated response to the messages list and returns the updated state.


2. After implementing the billing handler, follow the same pattern to implement the technical handler in `technical.py`. The handler should retrieve domain-specific knowledge from the appropriate section of the knowledge base (technical, product, general, or priority) and generate specialized responses tailored to their domain. 

	**Step 3.11**. Find the TODO comment: "Implement this handler following the pattern of the billing handler" and follow the steps below.
	
	**Step 3.12**. Find the TODO comment: "Extract message details" and add this code snippet:
	
	```python
	current_message = state["current_message"]
	content = current_message["content"]
	priority = current_message["priority"]
	user_name = current_message.get("user_name")
	additional_context = current_message.get("additional_context")
	```
	
	This code extracts the necessary details from the current message, including the content, priority level, user name, and any additional context provided.
	
	**Step 3.13**. Find the TODO comment: "Create personalized greeting and context acknowledgment" and add this code snippet:
	
	```python
	# Personalized greeting if name is provided
	greeting = f"Hello {user_name}, " if user_name else ""
	
	# Context acknowledgment if provided
	context_acknowledgment = ""
	if additional_context:
	    context_acknowledgment = (
	        f"Based on the additional context you provided ({additional_context}), "
	    )
	```
	
	This code creates a personalized greeting if a user name is available and acknowledges any additional context that was provided with the inquiry.
	
	**Step 3.14**. Find the TODO comment: "Get technical context from knowledge base" and add this code snippet:
	
	```python
	# Get context for technical inquiries
	technical_context = knowledge_base.get_context_for_prompt("technical")
	
	priority_note = ""
	if priority <= 2:
	    priority_note = " This is a high-priority technical issue that requires immediate attention."
	```
	
	This code retrieves technical-specific knowledge from the knowledge base and adds a priority note for high-priority issues (priority levels 1 or 2).
	
	**Step 3.15**. Find the TODO comment: "Create response prompt" and add this code snippet:
	
	```python
	response_prompt = f"""
	You are a technical support specialist helping a customer with their issue.{priority_note}
	
	IMPORTANT CONTEXT:
	{technical_context}
	
	Customer inquiry: {content}
	{f"Additional context: {additional_context}" if additional_context else ""}
	
	Provide a helpful, professional response addressing their technical problem.
	Include troubleshooting steps when appropriate.
	Reference specific company policies and procedures when applicable.
	
	IMPORTANT: Sign your response with the following format:
	
	Emma G.
	AI Customer Support Representative
	SaaS Solutions Inc.
	{f"Start with a personalized greeting: '{greeting}'" if user_name else ""}
	{f"Acknowledge the additional context: '{context_acknowledgment}'" if additional_context else ""}
	"""
	```
	
	This code creates a detailed prompt for the LLM that includes the technical context, customer inquiry, and instructions for formatting the response with personalization and proper signature.
	
	**Step 3.16**. Find the TODO comment: "Generate response and ensure proper signature" and add this code snippet:
	
	```python
	ollama_response = ollama_client.generate(response_prompt)
	response_str = ollama_response["response"]
	
	# Ensure the response has Emma's signature if it's missing
	if "Emma G." not in response_str:
	    response_str += (
	        "\n\nEmma G.\nAI Customer Support Representative\nSaaS Solutions Inc."
	    )
	```
	
	This code generates a response using the Ollama client and ensures that the response includes Emma's signature, adding it if necessary.
	
	**Step 3.17**. Find the TODO comment: "Update state with response and message status" and add this code snippet:
	
	```python
	# Update message status
	current_message["status"] = "resolved"
	state["current_message"] = current_message
	
	# Add to history
	state["history"].append(current_message)
	
	# Add response to messages
	state["messages"].append(AIMessage(content=response_str))
	```
	
	This code updates the message status to "resolved", adds the message to the history, and adds the AI's response to the messages list in the state.


3. After implementing the technical handler, follow the same pattern to implement the product handler in `product.py`. The handler should retrieve domain-specific knowledge from the appropriate section of the knowledge base (technical, product, general, or priority) and generate specialized responses tailored to their domain.  

    **Step 3.18**. Find the TODO comment: "Implement this handler following the pattern of the billing handler" and follow the steps below.
    
    **Step 3.19**. Find the TODO comment: "Extract information from current message" and add this code snippet:
    
    ```python
    current_message = state["current_message"]
    content = current_message["content"]
    user_name = current_message.get("user_name")
    additional_context = current_message.get("additional_context")

    # Personalized greeting if name is provided
    greeting = f"Hello {user_name}, " if user_name else ""

    # Context acknowledgment if provided
    context_acknowledgment = ""
    if additional_context:
        context_acknowledgment = (
            f"Based on the additional context you provided ({additional_context}), "
        )
    ```
    
    This code extracts the message content, user name, and additional context from the current message. It also creates a personalized greeting if a user name is provided and prepares a context acknowledgment if additional context is available.
    
    **Step 3.20**. Find the TODO comment: "Get product context from knowledge base" and add this code snippet:
    
    ```python
    # Get context for product inquiries
    product_context = knowledge_base.get_context_for_prompt("product")
    ```
    
    This code retrieves product-specific knowledge from the knowledge base to inform the response.
    
    **Step 3.21**. Find the TODO comment: "Create response prompt with product context" and add this code snippet:
    
    ```python
    response_prompt = f"""
    You are a product information specialist helping a customer learn more about our products.
    
    IMPORTANT CONTEXT:
    {product_context}
    
    Customer inquiry: {content}
    {f"Additional context: {additional_context}" if additional_context else ""}
    
    Provide a helpful, professional response with detailed product information.
    Reference specific product features, tiers, and pricing when applicable.
    
    IMPORTANT: Sign your response with the following format:
    
    Emma G.
    AI Customer Support Representative
    SaaS Solutions Inc.
    {f"Start with a personalized greeting: '{greeting}'" if user_name else ""}
    {f"Acknowledge the additional context: '{context_acknowledgment}'" if additional_context else ""}
    """
    ```
    
    This code creates a detailed prompt for the LLM that includes the product context, customer inquiry, and instructions for formatting the response with personalization and signature.
    
    **Step 3.22**. Find the TODO comment: "Generate response using Ollama" and add this code snippet:
    
    ```python
    ollama_response = ollama_client.generate(response_prompt)
    response_str = ollama_response["response"]

    # Ensure the response has Emma's signature if it's missing
    if "Emma G." not in response_str:
        response_str += (
            "\n\nEmma G.\nAI Customer Support Representative\nSaaS Solutions Inc."
        )
    ```
    
    This code sends the prompt to the Ollama client to generate a response and ensures the response includes Emma's signature.
    
    **Step 3.23**. Find the TODO comment: "Update state with response and message status" and add this code snippet:
    
    ```python
    # Update message status
    current_message["status"] = "resolved"
    state["current_message"] = current_message

    # Add to history
    state["history"].append(current_message)

    # Add response to messages
    state["messages"].append(AIMessage(content=response_str))
    ```
    
    This code updates the message status to "resolved", adds the current message to the history, and adds the AI response to the messages list in the state.
    
    **Step 3.24**. Find the TODO comment: "Return updated state" and add this code snippet:
    
    ```python
    return state
    ```
    
    This code returns the updated state with the new response and history.


4. After implementing the `product handler`, follow the same pattern to implement the general handler in `general.py`. The handler should retrieve domain-specific knowledge from the appropriate section of the knowledge base (technical, product, general, or priority) and generate specialized responses tailored to their domain. `

    **Step 3.25**. Find the TODO comment: "Implement this handler following the pattern of the billing handler" and follow the steps below.
    
    **Step 3.26**. Find the TODO comment: "Extract information from the current message" and add this code snippet:
    
    ```python
    current_message = state["current_message"]
    content = current_message["content"]
    user_name = current_message.get("user_name")
    additional_context = current_message.get("additional_context")
    ```
    
    This code extracts the message content, user name, and any additional context from the current message.
    
    **Step 3.27**. Find the TODO comment: "Create personalized greeting and context acknowledgment" and add this code snippet:
    
    ```python
    # Personalized greeting if name is provided
    greeting = f"Hello {user_name}, " if user_name else ""

    # Context acknowledgment if provided
    context_acknowledgment = ""
    if additional_context:
        context_acknowledgment = (
            f"Based on the additional context you provided ({additional_context}), "
        )
    ```
    
    This code creates a personalized greeting if a user name is provided and acknowledges any additional context.
    
    **Step 3.28**. Find the TODO comment: "Get general context from the knowledge base" and add this code snippet:
    
    ```python
    # Get context for general inquiries
    general_context = knowledge_base.get_context_for_prompt("general")
    ```
    
    This code retrieves general context information from the knowledge base to use in the response.
    
    **Step 3.29**. Find the TODO comment: "Create the prompt for the AI model" and add this code snippet:
    
    ```python
    response_prompt = f"""
    You are a customer service representative handling a general inquiry.
    
    IMPORTANT CONTEXT:
    {general_context}
    
    Customer inquiry: {content}
    {f"Additional context: {additional_context}" if additional_context else ""}
    
    Provide a helpful, professional response to their question or concern.
    Reference company information and policies when applicable.
    
    IMPORTANT: Sign your response with the following format:
    
    Emma G.
    AI Customer Support Representative
    SaaS Solutions Inc.
    {f"Start with a personalized greeting: '{greeting}'" if user_name else ""}
    {f"Acknowledge the additional context: '{context_acknowledgment}'" if additional_context else ""}
    """
    ```
    
    This code creates a detailed prompt for the AI model, including the general context, customer inquiry, and instructions for formatting the response.
    
    **Step 3.30**. Find the TODO comment: "Generate the response using the Ollama client" and add this code snippet:
    
    ```python
    ollama_response = ollama_client.generate(response_prompt)
    response_str = ollama_response["response"]

    # Ensure the response has Emma's signature if it's missing
    if "Emma G." not in response_str:
        response_str += (
            "\n\nEmma G.\nAI Customer Support Representative\nSaaS Solutions Inc."
        )
    ```
    
    This code generates a response using the Ollama client and ensures it includes Emma's signature.
    
    **Step 3.31**. Find the TODO comment: "Update the message status and history" and add this code snippet:
    
    ```python
    # Update message status
    current_message["status"] = "resolved"
    state["current_message"] = current_message

    # Add to history
    state["history"].append(current_message)

    # Add response to messages
    state["messages"].append(AIMessage(content=response_str))
    ```
    
    This code updates the message status to "resolved", adds the message to the history, and adds the AI response to the messages list.
    
    **Step 3.32**. Find the TODO comment: "Return the updated state" and add this code snippet:
    
    ```python
    return state
    ```
    
    This code returns the updated state object with all the changes made during the handling process.


5. After implementing the general handler, follow the same pattern to implement the priority handler in `priority.py`. Each handler should retrieve domain-specific knowledge from the appropriate section of the knowledge base (technical, product, general, or priority) and generate specialized responses tailored to their domain.  The priority handler requires special attention, as it should update the message status to "resolved_urgent" and include additional urgency acknowledgment in its responses. 

    **Step 3.33. Find the TODO comment: "Implement this handler following the pattern of the billing handler" and follow the steps below.
    
    **Step 3.34**. Find the TODO comment: "Extract message information" and add this code snippet:
    
    ```python
    current_message = state["current_message"]
    content = current_message["content"]
    message_type = current_message["type"]
    user_name = current_message.get("user_name")
    additional_context = current_message.get("additional_context")

    # Personalized greeting if name is provided
    greeting = f"Hello {user_name}, " if user_name else ""

    # Context acknowledgment if provided
    context_acknowledgment = ""
    if additional_context:
        context_acknowledgment = (
            f"Based on the additional context you provided ({additional_context}), "
        )
    ```
    
    This code extracts information from the current message including content, type, user name, and additional context. It also creates personalized greeting and context acknowledgment strings if applicable.
    
    **Step 3.35. Find the TODO comment: "Get knowledge base context" and add this code snippet:
    
    ```python
    # Get context for priority inquiries and the specific domain
    priority_context = knowledge_base.get_context_for_prompt("priority")
    domain_context = knowledge_base.get_context_for_prompt(message_type)
    ```
    
    This code retrieves specialized knowledge from both the priority section and the domain-specific section of the knowledge base.
    
    **Step 3.36**. Find the TODO comment: "Create prompt for urgent cases" and add this code snippet:
    
    ```python
    # Prepare a special prompt for urgent cases
    response_prompt = f"""
    You are a senior customer service representative handling an URGENT inquiry.
    This requires immediate attention and priority handling.
    
    The inquiry is related to: {message_type}
    
    PRIORITY HANDLING CONTEXT:
    {priority_context}
    
    DOMAIN-SPECIFIC CONTEXT:
    {domain_context}
    
    Customer inquiry: {content}
    {f"Additional context: {additional_context}" if additional_context else ""}
    
    Provide a detailed, reassuring response that acknowledges the urgency
    and offers a concrete next step or solution. Include information about
    expedited handling procedures for this priority case.
    Reference specific emergency procedures and escalation paths when applicable.
    
    IMPORTANT: Sign your response with the following format:
    
    Emma G.
    AI Customer Support Representative
    SaaS Solutions Inc.
    {f"Start with a personalized greeting: '{greeting}'" if user_name else ""}
    {f"Acknowledge the additional context: '{context_acknowledgment}'" if additional_context else ""}
    """
    ```
    
    This code creates a specialized prompt that emphasizes the urgency of the inquiry and includes both priority and domain-specific context. It also instructs the model to provide a reassuring response with concrete next steps and to sign the response appropriately.
    
    **Step 3.37**. Find the TODO comment: "Generate and format response" and add this code snippet:
    
    ```python
    ollama_response = ollama_client.generate(response_prompt)
    response_str = ollama_response["response"]

    # Ensure the response has Emma's signature if it's missing
    if "Emma G." not in response_str:
        response_str += (
            "\n\nEmma G.\nAI Customer Support Representative\nSaaS Solutions Inc."
        )
    ```
    
    This code generates a response using the Ollama client and ensures that the response includes Emma's signature, adding it if necessary.
    
    **Step 3.38**. Find the TODO comment: "Update state with response and status" and add this code snippet:
    
    ```python
    # Update message status
    current_message["status"] = "resolved_urgent"
    state["current_message"] = current_message

    # Add to history
    state["history"].append(current_message)

    # Add response to messages
    state["messages"].append(AIMessage(content=response_str))

    return state
    ```
    
    This code updates the message status to "resolved_urgent", adds the current message to the history, adds the AI response to the messages list, and returns the updated state.


### Task 4: Implement the Workflow Graph

For this next task, we'll implement the LangGraph workflow in the `workflow.py` file by completing the `create_customer_service_workflow` function. 
   
This function orchestrates the entire multi-agent system by defining the nodes, edges, and execution paths. This task demonstrates how to construct a directed graph with LangGraph that orchestrates the flow of information between multiple specialized agents.

   **Step 4.1**. Find the TODO comment: "Create a complete LangGraph workflow that:" and follow the steps below.
   
   **Step 4.2**. Find the TODO comment: "Initialize the StateGraph" and add this code snippet:
   
   ```python
    workflow = StateGraph(AgentState)
    ```
   
This code creates a new StateGraph object using the AgentState type, which will maintain conversation state throughout the workflow.
   
   **Step 4.3**. Find the TODO comment: "Add nodes to the graph with dependencies injected" and add this code snippet:
   
   ```python
    # Add nodes to the graph with dependencies injected
    workflow.add_node(
        "classifier", lambda state: classify_message(state, ollama_client)
    )
    workflow.add_node("router", route_message)
    workflow.add_node(
        "billing_handler",
        lambda state: handle_billing_inquiry(state, ollama_client, knowledge_base),
    )
    workflow.add_node(
        "technical_handler",
        lambda state: handle_technical_inquiry(state, ollama_client, knowledge_base),
    )
    workflow.add_node(
        "product_handler",
        lambda state: handle_product_inquiry(state, ollama_client, knowledge_base),
    )
    workflow.add_node(
        "general_handler",
        lambda state: handle_general_inquiry(state, ollama_client, knowledge_base),
    )
    workflow.add_node(
        "priority_handler",
        lambda state: handle_priority_inquiry(state, ollama_client, knowledge_base),
    )
    ```
   
   This code adds all necessary nodes to the graph, including the classifier node (with the Ollama client dependency injected), router node, and all five specialized handler nodes (each with both Ollama client and knowledge base dependencies injected).
   
   **Step 4.4**. Find the TODO comment: "Define the basic edges in the graph" and add this code snippet:
   
   ```python
    # Define the edges in the graph
    workflow.add_edge("classifier", "router")
    ```
   
   This code defines the sequential flow by adding a basic edge from the classifier to the router.
   
   **Step 4.5**. Find the TODO comment: "Add conditional edges from router to specialized handlers" and add this code snippet:
   
   ```python
    # Conditional edges from router to specialized handlers
    workflow.add_conditional_edges(
        "router",
        lambda x: x["next"],
        {
            "billing": "billing_handler",
            "technical": "technical_handler",
            "product": "product_handler",
            "general": "general_handler",
            "priority_handling": "priority_handler",
        },
    )
    ```

This code implements the dynamic branching logic using conditional edges from the router to the specialized handlers, mapping each possible router output to its corresponding handler node.

   **Step 4.6**. Find the TODO comment: "Connect all handlers to the END node" and add this code snippet:

   ```python
    # All handlers lead to END
    workflow.add_edge("billing_handler", END)
    workflow.add_edge("technical_handler", END)
    workflow.add_edge("product_handler", END)
    workflow.add_edge("general_handler", END)
    workflow.add_edge("priority_handler", END)
    ```

   This code connects all handler nodes to the END node, indicating that the workflow completes after a handler processes a message.

   **Step 4.7**. Find the TODO comment: "Set the entry point and compile the graph" and add this code snippet:

   ```python
    # Set the entry point
    workflow.set_entry_point("classifier")

    # Compile the graph
    return workflow.compile()
    ```
   
   This code sets the entry point of the workflow to the classifier node, establishing where execution begins for each new inquiry, and compiles the graph to create an executable workflow that can be invoked with an initial state.

### Task 5: Process Customer Inquiries

Next, we'll implement the main entry point for the system in the `workflow.py` file by implementing the `process_inquiry` function. 
   
This function serves as the bridge between the user interface and the internal workflow, handling all necessary initialization and execution. This task demonstrates how to initialize and execute a LangGraph workflow, managing state and dependencies throughout the process.
    
   **Step 5.1**. Find the TODO comment: "Implement this function to create the workflow, initialize the state, and invoke the workflow with the initial state" and follow the steps below.
    
   **Step 5.2**. Find the TODO comment: "Initialize the workflow" and add this code snippet:
    
   ```python
    # Initialize workflow
    workflow = create_customer_service_workflow(ollama_client, knowledge_base)
    ```
    
   This code creates the workflow graph by calling the `create_customer_service_workflow` function with the provided Ollama client and knowledge base.
    
   **Step 5.3**. Find the TODO comment: "Create initial state" and add this code snippet:
    
   ```python
    # Create initial state
    initial_state = AgentState(
        messages=[HumanMessage(content=message_content)],
        current_message={
            "content": message_content,
            "type": None,
            "priority": None,
            "status": "new",
            "user_name": user_name,
            "user_email": user_email,
            "additional_context": additional_context,
        },
        history=[],
    )
    ```
    
   This code initializes the workflow state by creating an `AgentState` object that includes the initial human message, a current message dictionary with all relevant fields (content, type, priority, status, and user information), and an empty history list. The current message starts with `None` values for type and priority (which will be determined by the classifier) and a status of "new".

   **Step 5.4**. Find the TODO comment: "Execute workflow and return result" and add this code snippet:

   ```python
    # Execute workflow
    result = workflow.invoke(initial_state)

    return result
    ```

This code invokes the workflow with the initial state, which triggers the execution of the entire processing pipeline—classification, routing, specialized handling, and response generation. It then returns the resulting state object, which contains the complete conversation history including all system messages and the AI-generated response.


## Testing Your Implementation

We're now ready to thoroughly test our implementation with different types of customer inquiries. 

Let's begin by running the application using `python app.py`, which launches an interactive console where you can enter customer inquiries and view the system's responses. 
   
Test with a variety of inquiry types from the provided test scenarios in `reference_docs/resources/test-scenarios.md`, including: 
   
- billing inquiries (e.g., "I was charged twice for my Pro subscription on April 1st"), 
- technical inquiries (e.g., "I'm locked out of my account after trying to reset my password"), 
- product inquiries (e.g., "Can you explain the main differences in storage limits between tiers?"), 
- general inquiries (e.g., "Where can I find documentation about your platform?"), 
- and priority inquiries (e.g., "EMERGENCY! All our client data has disappeared from our dashboard"). 
   
Verify that each inquiry is correctly classified by type and priority, routed to the appropriate specialized handler, and receives a personalized response that incorporates relevant knowledge base information and includes Emma G.'s signature. 

Test the personalization features by including optional user information in brackets (e.g., "[Name: Alex, Email: alex@example.com, Context: Enterprise customer]"). 

To streamline testing, use the demo mode by running `python app.py --demo`, which automatically executes a series of predefined test cases covering all handler types. This task ensures your implementation functions correctly across all possible customer inquiry scenarios.

Refer to the transcripts below to get an idea of how the demo and an example chat session work. To get you started with testing, use the provided test scenarios and observe the results.

- Demo Transcript -  [demo.md](demo.md) 
- Example Chat Session -  [example-chat-session.md](example-chat-session.md) 
- Test Scenarios -  [test-scenarios.md](resources\test-scenarios.md) 



## Extension Options

Here are some ways to extend this activity after completing the basic implementation:

1. **Multi-step Conversation Handling**
   - Implement a mechanism to handle follow-up questions within the same inquiry context
   - Create state transitions that can loop back to previous handlers

2. **Advanced Routing Logic**
   - Implement a more sophisticated routing algorithm that considers system load and agent availability
   - Create specialized paths for VIP customers or accounts with specific characteristics

3. **Performance Analytics**
   - Add instrumentation to track processing time at each node
   - Implement a dashboard that visualizes the flow of messages through the system



## Conclusion

This activity focuses on implementing a multi-agent workflow with LangGraph, a key component of building effective agent-based applications. we'll create a system that intelligently processes customer service inquiries by analyzing content, determining priority, and routing through appropriate specialized handlers. This reinforces the hub-and-spoke architecture pattern and demonstrates how to implement conditional execution paths in LangGraph workflows.
