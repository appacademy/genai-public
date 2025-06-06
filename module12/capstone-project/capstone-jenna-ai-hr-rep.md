# Capstone: Jenna - AI Human Resources Representative


## Overview

This capstone project focuses on building Jenna, an AI Human Resources Representative powered by modern language model technology. You'll implement a comprehensive HR assistant capable of answering questions about company policies and benefits, managing training records, and providing HR administrators with analytical insights about employee data. The system uses Retrieval-Augmented Generation (RAG) to deliver accurate, contextually appropriate responses across various HR domains, with specialized handling for sensitive workplace topics. Through this project, you'll gain practical experience implementing advanced NLP components including intent classification, conversation memory, specialized prompt engineering, and workflow orchestration with LangGraph.

## Learning Objectives

By completing this capstone project, you will be able to:

1. Implement a Retrieval-Augmented Generation (RAG) system that effectively retrieves and processes relevant information from a knowledge base of HR documents.
2. Design specialized prompt templates for different types of user queries to enhance response quality.
3. Develop an intent classification system that accurately categorizes user queries and extracts structured arguments for downstream processing.
4. Create a conversation memory system that maintains context across interactions and retrieves relevant history based on topic detection.
5. Fine-tune an LLM to improve performance on HR-specific tasks and ensure appropriate responses to sensitive workplace topics.
6. Orchestrate a complete HR assistant workflow using LangGraph to coordinate between different specialized components.

## Capstone Tasks 

In this project we will implement a complete HR assistant application that combines multiple AI capabilities to create a useful HR tool. We'll fine-tune a language model for HR-specific tasks, build specialized RAG systems for policy and benefits information, design a conversation memory system that maintains context across interactions, create an intent classification system to route queries correctly, and orchestrate everything with a directed graph workflow. Each component addresses specific challenges in building an effective HR assistant, from handling sensitive workplace topics appropriately to maintaining conversational context over multiple turns of interaction.

Begin by reading the [Jenna HR Assistant - Technical Documentation](_assets/tech-doc.md) .

### Capstone Task Phase 1: Fine-tune the Gemma 3 4B LLM

### Task 1: Fine-Tune Google Colab

Use the provided dataset.
Refer to the activity in Module 10 for instructions on fine-tuning the Gemma 3 4B LLM.


### Task 2: Convert Fine-Tuned LLM to GGUF Format

Refer to the activity in Module 10 for instructions on converting the fine-tuned LLM to GGUF on a local computer.


---
### Capstone Task Phase 2: Build the Application
### Setup Instructions

#### Step 1: Clone the Repository

Clone the starter code repository to your local machine:

```bash
git clone https://github.com/[organization]/multi-agent-problem-solver-starter.git
cd multi-agent-problem-solver-starter
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

- **Windows (Command Prompt)**:

```bash
  python -m venv .venv
  .venv\Scripts\activate
```

After activation, your terminal prompt should change (e.g., `(venv)` appears).



### Step 3: Install Dependencies

With the virtual environment active, install the required packages:

```bash
pip install -r requirements.txt
```

The requirements.txt file contains the following dependencies:

```
langchain>=0.1.0
langchain_community>=0.0.10
langchainhub>=0.1.14
langgraph>=0.0.20
faiss-cpu>=1.7.4
langchain-text-splitters>=0.0.1
sentence-transformers>=2.2.2
pandas>=2.0.0
pydantic>=2.4.0
python-dotenv>=1.0.0
typer>=0.9.0
rich>=13.6.0
langchain-ollama>=0.0.1
langchain-huggingface>=0.0.1
matplotlib>=3.5.0
seaborn>=0.12.0
networkx>=2.8.0
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

2. In a terminal window, start Ollama with the `gemma3finetuned:q4km` model:

   ```bash
   # All operating systems
   ollama run gemma3finetuned:q4km
   ```

   

### Task 1: Implement Intent Router

The `intent/router.py` file contains the `IntentRouter` class, which serves as the foundation for understanding user queries in the Jenna HR Assistant system. The primary TODO task involves enhancing the `classify` method to provide robust intent classification and argument extraction. 

The implementation must distinguish between various HR-related queries including policy questions, benefits inquiries, training record lookups, course enrollment requests, and HR data access requests. 

This intent classification system determines how user requests are routed to the appropriate handlers throughout the HR assistant workflow.

1. Locate the `IntentRouter` class in the `intent/router.py` file.

    **Step 1.1**. Find the TODO comment: "Implement the IntentRouter class to classify user queries into specific intents" and follow the steps below.
    
    **Step 1.2**. Find the TODO comment: "Implement the __init__ method to initialize the LLM and the prompt template" and add this code snippet:
    
    ```python
    def __init__(self, llm):
        self.llm = llm
        self.parser = JsonOutputParser(pydantic_object=Intent)
    ```
    
    This code initializes the IntentRouter with a language model and creates a JSON parser that will convert LLM responses into Intent objects.
    
    **Step 1.3**. Find the TODO comment: "Create a prompt template for intent classification" and add this code snippet:
    
    ```python
    # Creating the intent classification prompt
    self.prompt = ChatPromptTemplate.from_template(
        """
    You are an HR assistant tasked with classifying user queries into specific intents.
    Analyze the following query and classify it into one of these intents:
    - policy_q: Questions about company policies (e.g., "What's our PTO policy?", "Tell me about our substance abuse policy") OR follow-up questions about policies (e.g., "How does it compare to X?", "Tell me more about it")
    - benefit_q: Questions about employee benefits (e.g., "What's our 401(k) match?", "What wellness programs do we offer?") OR follow-up questions about benefits
    - train_lookup: Requests to view training records (e.g., "Show my training record")
    - train_courses: Requests to list available courses or course catalog (e.g., "What courses are available?", "List the required courses", "What training courses do you offer?")
    - train_enroll: Requests to enroll in training courses (e.g., "Enroll me in SEC-230")
    - train_update: Notifications about completed training (e.g., "I finished AI-201")
    - train_mandatory: Requests for all mandatory training (e.g., "Sign me up for all mandatory courses")
    - hr_employees: Requests to view all employee data (e.g., "Show me all employees", "Display employee directory", "List all staff")
    - hr_training: Requests to view all training records (e.g., "Show me all training records", "Display training data", "View master training file")
    - hr_employee_training: Requests to view specific employee's training (e.g., "Show training for Alice Johnson", "View Carlos's training status")
    - hr_bulk_add: Requests to add multiple employees at once (e.g., "Add these employees: E012 John Smith IT, E013 Jane Brown Marketing", "Bulk add employees")
    - hr_update: Requests to update employee information (e.g., "Update employee E021 role to Department Manager", "Change Emma Jackson's department to Operations")
    - hr_analytics: Requests for HR analytics and statistics (e.g., "How many people have completed HR-001?", "Show department statistics", "Which employees haven't finished SEC-010?")
    - fallback: Any query not related to HR functions (e.g., "What's the weather?", "Tell me a joke")
    
    IMPORTANT: Questions about wellness programs, substance abuse, addiction support, mental health services, Employee Assistance Programs (EAP), and other sensitive HR topics should be classified as either policy_q or benefit_q depending on the nature of the question, NOT as fallback.
    
    For train_enroll, train_update, and train_mandatory, extract any relevant arguments.
    
    Examples:
    - "What's the weather today?" → {{"intent": "fallback"}}
    - "Tell me a joke" → {{"intent": "fallback"}}
    - "What's our PTO policy?" → {{"intent": "policy_q"}}
    - "Tell me about substance abuse policy" → {{"intent": "policy_q"}}
    - "What options do I have for addiction help?" → {{"intent": "policy_q"}}
    - "Does the wellness program address addiction?" → {{"intent": "benefit_q"}}
    - "Tell me about our Employee Assistance Program" → {{"intent": "benefit_q"}}
    - "What mental health resources are available?" → {{"intent": "benefit_q"}}
    - "Which takes precedence, Substance Abuse Policy or EAP?" → {{"intent": "policy_q"}}
    - "What courses are available?" → {{"intent": "train_courses"}}
    - "Can you list the required courses?" → {{"intent": "train_courses"}}
    - "What training do I need to take?" → {{"intent": "train_courses"}}
    - "Enroll me in SEC-230" → {{"intent": "train_enroll", "args": {{"course_ids": ["SEC-230"]}}}}
    - "Enroll me in SEC-230 and AI-201" → {{"intent": "train_enroll", "args": {{"course_ids": ["SEC-230", "AI-201"]}}}}
    - "I finished AI-201 yesterday" → {{"intent": "train_update", "args": {{"course_ids": ["AI-201"]}}}}
    - "I completed HR-001 and SEC-010" → {{"intent": "train_update", "args": {{"course_ids": ["HR-001", "SEC-010"]}}}}
    - "Add these employees: E012 John Smith IT, E013 Jane Doe HR" → {{"intent": "hr_bulk_add", "args": {{"employees": [
        {{"employee_id": "E012", "name": "John Smith", "department": "IT"}},
        {{"employee_id": "E013", "name": "Jane Doe", "department": "HR"}}
      ]}}}}
    - "Bulk add employees E014 Robert Jones Engineering and E015 Maria Garcia Marketing" → {{"intent": "hr_bulk_add", "args": {{"employees": [
        {{"employee_id": "E014", "name": "Robert Jones", "department": "Engineering"}},
        {{"employee_id": "E015", "name": "Maria Garcia", "department": "Marketing"}}
      ]}}}}
    - "Update employee E021 role to Department Manager" → {{"intent": "hr_update", "args": {{"employee_id": "E021", "role": "Department Manager"}}}}
    - "Change Emma Jackson's department to Operations" → {{"intent": "hr_update", "args": {{"employee_id": "E021", "name": "Emma Jackson", "department": "Operations"}}}}
    - "Set E015 start date to 2025-01-15" → {{"intent": "hr_update", "args": {{"employee_id": "E015", "start_date": "2025-01-15"}}}}
    - "Update James Anderson to the role of Senior Account Executive" → {{"intent": "hr_update", "args": {{"employee_id": "E020", "name": "James Anderson", "role": "Senior Account Executive"}}}}
    
    User query: {query}
    
    Classification (output as JSON):
    """
    )
    ```
    
    This code creates a detailed prompt template that instructs the LLM how to classify different HR-related queries into specific intents. It includes examples of each intent type and special handling for sensitive HR topics.
    
    **Step 1.4**. Find the TODO comment: "Create a chain that combines the prompt, LLM, and parser" and add this code snippet:
    
    ```python
    self.chain = self.prompt | self.llm | self.parser
    ```
    
    This code creates a processing chain that will: 1) format the prompt with the user query, 2) send it to the language model, and 3) parse the JSON response into an Intent object.
    
    **Step 1.5**. Find the TODO comment: "Implement the classify method to classify user queries into specific intents" and add this code snippet:
    
    ```python
    def classify(self, query):
        """Classify a user query into an intent"""
        return self.chain.invoke({"query": query})
    ```
    
    This code implements the classify method that takes a user query, passes it through the chain created earlier, and returns the classified intent with any extracted arguments.



### Task 2: Implement LangGraph Workflow for Orchestration

The `orchestration/graph.py` file is responsible for creating the LangGraph workflow that orchestrates the entire HR assistant system. The primary TODO task involves implementing the `create_workflow` function, which constructs a directed graph of nodes representing different processing steps. 

The function initializes a StateGraph with GraphState, setting up conversation memory and diagnostics. It defines node wrappers that inject dependencies for HR assistant functions like intent classification, policy Q&A, training record management, and HR data access. The workflow adds nodes to the graph, starts with intent classification, and establishes conditional edges to route queries to appropriate handlers based on intent. This orchestration layer ensures queries flow logically through specialized handlers for different HR requests, all ultimately terminating at the END state.

**Step 2.1**. Find the TODO comment: "Implement the create_workflow function to create the LangGraph workflow for orchestrating the HR assistant" and add this code snippet:

```python
def create_workflow(intent_router, policy_rag, benefits_rag, training_records, llm):
    """Create the LangGraph workflow for orchestrating the HR assistant."""
    workflow = StateGraph(GraphState)

    # Initialize conversation memory and diagnostics
    memory = ConversationMemory()
    diagnostics = ConversationDiagnostics()
```

This code initializes the LangGraph workflow with the GraphState model and sets up conversation memory and diagnostics components.

**Step 2.2**. Find the TODO comment: "Define node wrappers that inject dependencies" and add this code snippet:

```python
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
```

This code defines node wrapper functions that inject dependencies for various HR assistant functions, including intent classification, policy and benefits question answering, training record management, and HR data access.

**Step 2.3**. Find the TODO comment: "Add nodes to the workflow" and add this code snippet:

```python
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
```

This code adds all the node wrapper functions to the workflow graph, giving each a unique name that identifies its purpose.

**Step 2.4**. Find the TODO comment: "Set the entry point of the workflow" and add this code snippet:

```python
    # Define edges
    workflow.set_entry_point("classify_intent")
```

This code sets the entry point of the workflow to the intent classification node, which is the first step in processing any user query.

**Step 2.5**. Find the TODO comment: "Define edges between nodes" and add this code snippet:

```python
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
```

This code establishes conditional edges that route user queries from the intent classification node to appropriate handlers based on the classified intent.

**Step 2.6**. Find the TODO comment: "Connect all terminal nodes to END" and add this code snippet:

```python
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
```

This code connects all handler nodes to the END state, indicating that processing terminates after a handler has processed the user query.

**Step 2.7**. Find the TODO comment: "Return the compiled workflow" and add this code snippet:

```python
    return workflow.compile()
```

This code compiles and returns the workflow, making it ready for execution.



### Task 3: Implement Conversation Memory System

The `orchestration/memory.py` file contains the conversation memory system that maintains state across interactions. The file includes two key classes: `Conversation` and `ConversationMemory`. The TODO tasks focus on implementing methods to manage conversation history, detect topics, calculate relevance scores, and retrieve relevant history for context. 

The `Conversation` class needs methods to add interactions, retrieve previous ones with filtering, detect topics, calculate relevance, extract entities, and create summaries.

The `ConversationMemory` class requires methods to update memory, retrieve relevant history, get summaries, extract entities, save snapshots, and generate reports.

Critical is the `get_relevant_history` method, which must intelligently retrieve conversation history by detecting topic switches, retrieving topic-relevant history with good relevance scores, and falling back to recent history when needed. This system maintains context across multiple turns, enabling coherent and contextually appropriate responses.

   **Step 3.1**. Find the TODO comment: "Implement the Conversation class to manage conversation history and diagnostics" and follow the steps below.

   **Step 3.2**. Find the TODO comment: "Implement the __init__ method to initialize conversation history and settings" and add this code snippet:

   ```python
    def __init__(
        self,
        max_history_items=10,
        history_folder="training/conversation_history",
        log_folder="logs",
    ):
        """Initialize conversation history manager"""
        self.conversation_history = []
        self.max_history_items = max_history_items
        self.history_folder = history_folder
        self.log_folder = log_folder

        # Create folders if they don't exist
        os.makedirs(history_folder, exist_ok=True)
        os.makedirs(log_folder, exist_ok=True)

        # Initialize relevance scoring metrics
        self.topic_keywords = {
            "policy": [
                "policy",
                "policies",
                "procedure",
                "rule",
                "guideline",
                "compliance",
            ],
            "benefit": [
                "benefit",
                "benefits",
                "insurance",
                "coverage",
                "compensation",
                "perks",
            ],
            "pto": ["pto", "vacation", "time off", "leave", "holiday", "break"],
            "health": ["health", "medical", "doctor", "treatment", "wellness", "care"],
            "retirement": ["401k", "retirement", "pension", "savings", "future"],
            "training": [
                "training",
                "course",
                "development",
                "learning",
                "education",
                "skill",
            ],
        }
   ```

   This code initializes the conversation history manager with settings for maximum history items and folders for storing history and logs. It creates the necessary folders and sets up topic keywords for relevance scoring.

   **Step 3.3**. Find the TODO comment: "Implement the add_interaction method to add a new interaction to the conversation history" and add this code snippet:

   ```python
    def add_interaction(
        self,
        question: str,
        response: str,
        context: List[Dict[str, Any]],
        intent: Dict[str, Any],
        conversation_topic: str = None,
    ):
        """Add a new interaction to the conversation history"""
        # Generate a timestamp
        timestamp = datetime.datetime.now().isoformat()

        # Detect topics if not provided
        detected_topics = (
            conversation_topic if conversation_topic else self.detect_topics(question)
        )

        # Calculate relevance score for this interaction (0-100 scale)
        relevance_score = self.calculate_context_relevance(question, context)

        # Extract key entities from question and response
        entities = self.extract_entities(question, response)

        # Create interaction summary
        summary = self.summarize_interaction(question, response, detected_topics)

        # Create the interaction object
        interaction = {
            "timestamp": timestamp,
            "question": question,
            "response": response,
            "context_ids": (
                [self._get_context_id(ctx) for ctx in context] if context else []
            ),
            "intent": intent,
            "topics": detected_topics,
            "relevance_score": relevance_score,
            "entities": entities,
            "summary": summary,
        }

        # Add to history
        self.conversation_history.append(interaction)

        # Trim history if it exceeds max size
        if len(self.conversation_history) > self.max_history_items:
            self.conversation_history = self.conversation_history[
                -self.max_history_items :
            ]

        # Log the interaction
        self._log_interaction(interaction)

        return interaction
   ```

   This code adds a new interaction to the conversation history. It generates a timestamp, detects topics, calculates relevance scores, extracts entities, creates a summary, and logs the interaction.

   **Step 3.4**. Find the TODO comment: "Implement the get_previous_interactions method to retrieve previous interactions" and add this code snippet:

   ```python
    def get_previous_interactions(self, count=3, topic_filter=None, min_relevance=None):
        """Get previous interactions, with optional filtering"""
        filtered_history = self.conversation_history

        # Apply topic filter if provided
        if topic_filter:
            filtered_history = [
                interaction
                for interaction in filtered_history
                if topic_filter in interaction.get("topics", [])
            ]

        # Apply relevance filter if provided
        if min_relevance is not None:
            filtered_history = [
                interaction
                for interaction in filtered_history
                if interaction.get("relevance_score", 0) >= min_relevance
            ]

        # Return the most recent items up to count
        return filtered_history[-count:]
   ```

   This code retrieves previous interactions from the conversation history, with optional filtering by topic and minimum relevance score.

   **Step 3.5**. Find the TODO comment: "Implement the detect_topics method to detect topics in text based on keywords" and add this code snippet:

   ```python
    def detect_topics(self, text):
        """Detect topics in text based on keywords"""
        if not text:
            return []

        text_lower = text.lower()
        detected_topics = []

        for topic, keywords in self.topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_topics.append(topic)

        return detected_topics
   ```

   This code detects topics in text based on keywords defined in the topic_keywords dictionary.

   **Step 3.6**. Find the TODO comment: "Implement the calculate_context_relevance method to calculate relevance score between query and context" and add this code snippet:

   ```python
    def calculate_context_relevance(self, query, context):
        """Calculate relevance score between query and retrieved context"""
        if not query or not context:
            return 0

        # Simple implementation based on term overlap
        query_terms = set(query.lower().split())

        total_score = 0
        for ctx in context:
            # Get content text from context
            content = (
                ctx.get("page_content", "")
                if isinstance(ctx, dict)
                else getattr(ctx, "page_content", "")
            )

            if content:
                # Count overlapping terms
                content_terms = set(content.lower().split())
                overlap = len(query_terms.intersection(content_terms))

                # Calculate score (0-100)
                ctx_score = min(100, int((overlap / max(1, len(query_terms))) * 100))
                total_score += ctx_score

        # Average the scores
        avg_score = int(total_score / max(1, len(context)))
        return avg_score
   ```

   This code calculates a relevance score between a query and retrieved context based on term overlap, returning a score from 0 to 100.

   **Step 3.7**. Find the TODO comment: "Implement the extract_entities method to extract key entities from question and response" and add this code snippet:

   ```python
    def extract_entities(self, question, response):
        """Extract key entities from question and response"""
        entities = {"policies": [], "benefits": [], "dates": [], "numbers": []}

        # Handle case where either might be None
        question = question or ""
        response = response or ""

        # Simple keyword-based extraction
        text = question + " " + response
        text_lower = text.lower()

        # Extract policies
        policy_keywords = ["policy", "procedure", "guideline", "rule"]
        for keyword in policy_keywords:
            if keyword in text_lower:
                idx = text_lower.find(keyword)
                if idx >= 0:
                    # Try to extract policy name by looking at surrounding words
                    start = max(0, idx - 20)
                    end = min(len(text_lower), idx + 30)
                    policy_fragment = text[start:end]
                    entities["policies"].append(policy_fragment.strip())

        # Extract benefits
        benefit_keywords = [
            "insurance",
            "medical",
            "dental",
            "vision",
            "401k",
            "retirement",
        ]
        for keyword in benefit_keywords:
            if keyword in text_lower:
                entities["benefits"].append(keyword)

        # Simple number detection
        import re

        # Find numbers in text
        numbers = re.findall(r"\b\d+\b", text)
        entities["numbers"] = numbers[:5]  # Limit to first 5 numbers

        # Simple date detection for common formats
        date_patterns = [
            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",  # MM/DD/YYYY
            r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",  # MM-DD-YYYY
            r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b",  # January 1, 2025
        ]

        for pattern in date_patterns:
            dates = re.findall(pattern, text, re.IGNORECASE)
            if dates:
                entities["dates"].extend(dates)

        # Remove duplicates while preserving order
        for key in entities:
            entities[key] = list(dict.fromkeys(entities[key]))

        return entities
   ```

   This code extracts key entities from question and response text, including policies, benefits, dates, and numbers using keyword matching and regular expressions.

   **Step 3.8**. Find the TODO comment: "Implement the summarize_interaction method to create a summary of the interaction" and add this code snippet:

   ```python
    def summarize_interaction(self, question, response, topics):
        """Create a summary of the interaction"""
        # Handle null values
        if not question:
            question = ""
        if not response:
            response = ""
        if not topics:
            topics = ["general"]

        # Simple summary creation - in a real system this could use an actual summarization model
        summary = (
            f"Question about {', '.join(topics) if topics else 'general HR topics'}"
        )

        # Add word count
        question_words = len(question.split())
        response_words = len(response.split())
        summary += f". {question_words} word question, {response_words} word response"

        return summary
   ```

   This code creates a simple summary of the interaction, including the topics discussed and the word count of the question and response.

   **Step 3.9**. Find the TODO comment: "Implement the get_relevant_history method to retrieve relevant conversation history" and add this code snippet:

   ```python
    def get_relevant_history(self, query, topic=None, count=3):
        """Get relevant conversation history for the current query"""
        # If topic switching was detected, prioritize recent history
        if self.topic_switching_detected:
            return self.conversation.get_previous_interactions(count=count)

        # Otherwise, try to get topic-relevant history with good relevance
        topic_filter = topic or self.current_topic
        relevant_history = self.conversation.get_previous_interactions(
            count=count, topic_filter=topic_filter, min_relevance=50
        )

        # Fall back to recent history if no relevant history found
        if not relevant_history:
            relevant_history = self.conversation.get_previous_interactions(count=count)

        return relevant_history
   ```

   This code retrieves relevant conversation history for the current query, considering topic switching, topic relevance, and relevance scores.



### Task 4: Implement Conversation State

The `orchestration/state.py` file defines the `GraphState` class, which is a Pydantic model that manages the state of the conversation throughout the workflow. The TODO tasks involve defining the fields that will store all relevant information as the user query progresses through the system. 

The implementation requires basic fields including raw user input, classified intent, retrieved RAG context, and final response. The state tracks employee data (ID, name, department, role, new status) and conversation history (previous question, context, response, and current topic). This state object flows through the LangGraph workflow, with each node processing the current state and returning an updated version. The `GraphState` class enables information to pass between components and maintains context for coherent multi-turn conversations.

   **Step 4.1**. Find the TODO comment: "Implement the GraphState class to manage the state of the conversation" and follow the steps below.

   **Step 4.2**. Find the TODO comment: "Define basic fields for tracking conversation state" and add this code snippet:

   ```python
    # Basic fields
    user_input: str = Field(description="The raw user input text")
    intent: Optional[Dict[str, Any]] = Field(None, description="The classified intent")
    context: Optional[List[Dict[str, Any]]] = Field(
        None, description="Retrieved context for RAG"
    )
    response: Optional[str] = Field(
        None, description="The final response to return to the user"
    )
   ```

   This code defines the basic fields that track the essential elements of each conversation turn: the user's input text, the classified intent of their query, any context retrieved for RAG (Retrieval Augmented Generation), and the final response that will be returned to the user.

   **Step 4.3**. Find the TODO comment: "Define employee information fields" and add this code snippet:

   ```python
    # Employee information
    employee_id: str = Field("current_user", description="The current employee ID")
    employee_name: Optional[str] = Field(None, description="The employee's name")
    is_new_employee: bool = Field(
        False, description="Whether the employee is new (< 7 days)"
    )
    department: Optional[str] = Field(None, description="The employee's department")
    role: Optional[str] = Field(None, description="The employee's role")
   ```

   This code defines fields to store information about the employee using the system, including their ID (defaulting to "current_user"), name, new employee status, department, and role. This information helps personalize responses.

   **Step 4.4**. Find the TODO comment: "Define conversation history fields" and add this code snippet:

   ```python
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
   ```

   This code defines fields that maintain the conversation history, including the previous question asked by the user, the context used in previous interactions, the previous response provided by the system, and the current topic of conversation. These fields enable the system to maintain context across multiple conversation turns.


### Task 5: Implement Orchestration Utilities

The `orchestration/utils.py` file provides utility functions that support the orchestration process. The primary TODO tasks involve implementing the `classify_topic` function and the `log_processing_time` function. 

The `classify_topic` function needs to classify the conversation topic based on the query text and intent, using a mapping of keywords to topics. It should return an appropriate topic label that can be used by the memory system to organize and retrieve relevant conversation history. 

The `log_processing_time` function is a simpler utility that logs the processing time of various functions, which is useful for performance monitoring and debugging. These utility functions support the overall orchestration system by providing common functionality that can be used across different components, enhancing the system's ability to understand conversation context and monitor performance.

   **Step 5.1**. Find the TODO comment: "Implement the classify_topic function to classify the topic of conversation" and follow the steps below.

   **Step 5.2**. Find the TODO comment: "1. Define a mapping of keywords to topics" and add this code snippet:

   ```python
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
   ```

   This code creates a dictionary that maps specific keywords to their corresponding topics. It also converts the query text to lowercase for case-insensitive matching.

   **Step 5.3**. Find the TODO comment: "2. Check if the intent already provides a topic" and add this code snippet:

   ```python
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
   ```

   This code first checks if the intent already indicates a topic. For policy questions, it tries to determine the specific policy type by checking for keywords. For benefit questions or training-related intents, it returns the corresponding topic. If the intent doesn't provide a topic, it checks the query text for keywords and returns the matching topic. If no match is found, it returns "general".

   **Step 5.4**. Find the TODO comment: "Implement the log_processing_time function to log the processing time of a function" and add this code snippet:

   ```python
    total_time = time.time() - start_time
    print(f"{func_name} completed in {total_time:.3f}s")
   ```

   This code calculates the total processing time by subtracting the start time from the current time, then prints a message showing which function was executed and how long it took, formatted to three decimal places.



### Task 6: Implement Intent Classification Nodes

The `classification_nodes.py` file contains the implementation of the intent classification node for the HR assistant orchestration graph. The primary TODO task involves implementing the `classify_intent` function, which processes user queries to determine their intent. 

This function starts a performance timer, uses the intent router to classify user input, and determines the conversation topic. It logs processing information including follow-up status and detected entities, as well as processing time. The function returns a dictionary with the classified intent and conversation topic, which the orchestration graph uses to route queries to appropriate handlers. This classification node serves as the entry point for all user queries, determining how the system responds to different request types.

   **Step 6.1**. Find the TODO comment: "Implement the classify_intent function to classify the intent of the user query" and follow the steps below.

   **Step 6.2**. Find the TODO comment: "1. Initialize the start time for processing" and add this code snippet:

   ```python
    start_time = time.time()
   ```

   This code initializes a timestamp to track how long the intent classification process takes.

   **Step 6.3**. Find the TODO comment: "2. Classify the intent" and add this code snippet:

   ```python
    intent_data = intent_router.classify(state.user_input)
   ```

   This code uses the intent router to analyze the user's input and determine what they're trying to accomplish.

   **Step 6.4**. Find the TODO comment: "3. Determine conversation topic" and add this code snippet:

   ```python
    conversation_topic = classify_topic(state.user_input, intent_data)
   ```

   This code identifies the specific topic of conversation based on the user's query and the classified intent.

   **Step 6.5**. Find the TODO comment: "4. Log query processing information" and add this code snippet:

   ```python
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=(state.previous_question is not None),
        detected_entities=intent_data.get("entities", []),
    )
   ```

   This code logs information about the query processing, including whether it's a follow-up question and any entities detected in the user's input.

   **Step 6.6**. Find the TODO comment: "5. Log the processing time" and add this code snippet:

   ```python
    log_processing_time("Intent classification", start_time)
   ```

   This code logs how long the intent classification process took for performance monitoring.

   **Step 6.7**. Find the TODO comment: "6. Return the classification results" and add this code snippet:

   ```python
    return {"intent": intent_data, "conversation_topic": conversation_topic}
   ```

   This code returns a dictionary containing the classified intent and conversation topic, which will be used by the orchestration graph to route the query to the appropriate handler.



### Task 7: Implement Benefits Question Answering Nodes

The `benefits_nodes.py` file contains the implementation of the benefits question answering node for the HR assistant orchestration graph. The primary TODO task involves implementing the `benefits_qa` function, which generates responses to benefits-related questions. 

This function starts a timer and stores the current query. It checks if the query is a follow-up and retrieves relevant conversation history. The implementation logs query details (follow-up status, comparative nature, sensitivity). It retrieves documents from the benefits RAG system, logs metrics, and combines current context with previous context for follow-ups to maintain continuity. The function generates a response, updates conversation memory, logs processing time, and returns a dictionary with context, response, and previous state information. This node provides accurate, contextually appropriate responses to employee questions about benefits, insurance, retirement plans, and HR benefits.

   **Step 7.1**. Find the TODO comment: "Implement the benefits_qa function to handle benefits-related questions" and follow the steps below.

   **Step 7.2**. Find the TODO comment: "1. Initialize the start time for processing" and add this code snippet:

   ```python
    start_time = time.time()
   ```

   This code initializes a timer to track how long the function takes to process the request.

   **Step 7.3**. Find the TODO comment: "2. Check if the user input is empty or None" and add this code snippet:

   ```python
    # Store the current query for next time
    previous_question = state.user_input
   ```

   This code stores the current user query so it can be referenced in future interactions.

   **Step 7.4**. Find the TODO comment: "3. Check if this is a follow-up question" and add this code snippet:

   ```python
    is_follow_up = state.previous_question and benefits_rag.is_followup_question(
        state.user_input, state.previous_question
    )
   ```

   This code determines if the current question is a follow-up to a previous question by comparing them using the benefits_rag system.

   **Step 7.5**. Find the TODO comment: "4. Get relevant history from memory" and add this code snippet:

   ```python
    relevant_history = (
        memory.get_relevant_history(
            state.user_input, topic=state.conversation_topic, count=3
        )
        if state.previous_question
        else []
    )
   ```

   This code retrieves up to 3 relevant previous interactions from memory if this is not the first question in the conversation.

   **Step 7.6**. Find the TODO comment: "5. Log the query details" and add this code snippet:

   ```python
    diagnostics.log_query_processing(
        query=state.user_input,
        expanded_query=None,  # We'll update this after retrieval
        is_followup=is_follow_up,
        is_comparative=benefits_rag.is_comparative_question(state.user_input),
        is_sensitive=benefits_rag.is_sensitive_topic(state.user_input),
    )
   ```

   This code logs details about the query, including whether it's a follow-up question, a comparative question, or about a sensitive topic.

   **Step 7.7**. Find the TODO comment: "6. Get context for the current query" and add this code snippet:

   ```python
    retrieval_start = time.time()
    context = benefits_rag.get_relevant_documents(state.user_input)
    retrieval_time = time.time() - retrieval_start
   ```

   This code retrieves relevant documents for the current query and measures how long the retrieval process takes.

   **Step 7.8**. Find the TODO comment: "7. Log the context retrieval details" and add this code snippet:

   ```python
    diagnostics.log_context_retrieval(retrieval_time=retrieval_time, documents=context)
   ```

   This code logs metrics about the context retrieval process, including the time taken and the documents retrieved.

   **Step 7.9**. Find the TODO comment: "8. If this appears to be a follow-up question, include previous context" and add this code snippet:

   ```python
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
   ```

   This code combines the current context with previous context if this is a follow-up question, and also includes context from relevant history if available.

   **Step 7.10**. Find the TODO comment: "9. Generate response with the appropriate context" and add this code snippet:

   ```python
    response = benefits_rag.generate_response(
        state.user_input,
        combined_context,
        previous_question=state.previous_question,
        previous_context=state.previous_context,
    )
   ```

   This code generates a response to the user's question using the combined context and information about previous interactions.

   **Step 7.11**. Find the TODO comment: "10. Update memory with this interaction" and add this code snippet:

   ```python
    memory.update(state)

    if is_follow_up:
        memory_report = memory.generate_diagnostics_report()
        print("\nMemory System Report:")
        print(memory_report)
   ```

   This code updates the conversation memory with the current interaction and generates a memory diagnostics report if this is a follow-up question.

   **Step 7.12**. Find the TODO comment: "11. Log the response generation details" and add this code snippet:

   ```python
    log_processing_time("Benefits QA", start_time)
   ```

   This code logs the total processing time for the benefits question answering function.

   **Step 7.13**. Find the TODO comment: "12. Store current state as previous for next query" and add this code snippet:

   ```python
    return {
        "context": context,
        "response": response,
        "previous_question": previous_question,
        "previous_context": context,
        "previous_response": response,
    }
   ```

   This code returns a dictionary containing the context, response, and previous state information that will be used for the next interaction.



### Task 8: Implement Policy Question Answering Nodes

The `policy_nodes.py` file contains the implementation of the policy question answering node for the HR assistant orchestration graph. The primary TODO task involves implementing the `policy_qa` function, which generates responses to policy-related questions. 

This function sets a timer, stores the query, checks for follow-ups, retrieves relevant history, and logs query details. It fetches documents from the policy RAG system, logs metrics, and combines current context with previous context for follow-ups to maintain continuity. The function generates a response using the policy RAG system, updates conversation memory, logs processing time, and returns context, response, and previous state information. This node answers employee questions about company policies, procedures, and guidelines, ensuring accurate, up-to-date information about workplace rules and expectations.

   **Step 8.1**. Find the TODO comment: "Implement the policy_qa function to handle policy-related questions" and follow the steps below.

   **Step 8.2**. Find the TODO comment: "1. Initialize the start time for processing and store the current query" and add this code snippet:

   ```python
    start_time = time.time()

    # Store the current query for next time
    previous_question = state.user_input
   ```

   This code initializes a timestamp to track processing time and stores the current user input for reference in future interactions.

   **Step 8.3**. Find the TODO comment: "2. Check if this is a follow-up question and get relevant history from memory" and add this code snippet:

   ```python
    # Check if this is a follow-up question
    is_follow_up = state.previous_question and policy_rag.is_followup_question(
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
   ```

   This code determines if the current question is a follow-up to a previous question and retrieves relevant conversation history from memory to maintain context.

   **Step 8.4**. Find the TODO comment: "3. Log the query details" and add this code snippet:

   ```python
    # Log the query details
    diagnostics.log_query_processing(
        query=state.user_input,
        expanded_query=None,  # We'll update this after retrieval
        is_followup=is_follow_up,
        is_comparative=policy_rag.is_comparative_question(state.user_input),
        is_sensitive=policy_rag.is_sensitive_topic(state.user_input),
    )
   ```

   This code logs details about the query for diagnostic purposes, including whether it's a follow-up, comparative, or sensitive question.

   **Step 8.5**. Find the TODO comment: "4. Get context for the current query and log the context retrieval details" and add this code snippet:

   ```python
    # Get context for the current query
    retrieval_start = time.time()
    context = policy_rag.get_relevant_documents(state.user_input)
    retrieval_time = time.time() - retrieval_start

    # Log retrieval metrics
    diagnostics.log_context_retrieval(retrieval_time=retrieval_time, documents=context)
   ```

   This code retrieves relevant policy documents for the current query, measures the retrieval time, and logs metrics about the retrieved context.

   **Step 8.6**. Find the TODO comment: "5. If this appears to be a follow-up question, include previous context" and add this code snippet:

   ```python
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
   ```

   This code combines the current context with previous context for follow-up questions to maintain conversation continuity, and also includes context from relevant history if available.

   **Step 8.7**. Find the TODO comment: "6. Generate response with the appropriate context and update memory" and add this code snippet:

   ```python
    # Generate response with the appropriate context
    response = policy_rag.generate_response(
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
   ```

   This code generates a response using the policy RAG system with the appropriate context, updates the conversation memory, and generates a memory diagnostics report for follow-up questions.

   **Step 8.8**. Find the TODO comment: "7. Log the processing time and return the response" and add this code snippet:

   ```python
    log_processing_time("Policy QA", start_time)

    # Store current state as previous for next query
    return {
        "context": context,
        "response": response,
        "previous_question": previous_question,
        "previous_context": context,
        "previous_response": response,
    }
   ```

   This code logs the total processing time and returns a dictionary containing the context, response, and previous state information for the next interaction.



### Task 9: Implement HR Administration Nodes

The `hr_nodes.py` file contains implementations for several HR administration nodes that handle employee data and training records. 

The TODO tasks include implementing six key functions: `hr_employees` (employee directory access), `hr_training` (viewing all training records), `hr_employee_training` (viewing specific employee training), `hr_update_employee` (updating employee information), `hr_bulk_add_employees` (adding multiple employees), and `hr_analytics` (generating HR data analytics).

Each function follows a pattern: setting a timer, logging the request, checking permissions (typically limited to Jane Doe), processing the HR task, generating a formatted response, updating memory, and logging processing time.

The `hr_analytics` function handles various analytical queries including training completion statistics, department breakdowns, and new employee analytics. These nodes provide HR administrative functionality with proper authentication to ensure sensitive HR data remains accessible only to authorized personnel.

1. **Locate the HR administration functions in the `hr_nodes.py` file.**

   **Step 1.1**. Find the TODO comment: "Implement the hr_employees function to handle employee directory requests" and follow the steps below.

   **Step 1.2**. Find the TODO comment: "1. Initialize the start time for processing" and add this code snippet:

   ```python
    start_time = time.time()
   ```

   This code initializes a timer to track how long the function takes to execute.

   **Step 1.3**. Find the TODO comment: "2. Log the request" and add this code snippet:

   ```python
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "employee_directory"],
    )
   ```

   This code logs the user's request with diagnostic information for tracking purposes.

   **Step 1.4**. Find the TODO comment: "3. Check if the user is Jane Doe (E002), the HR representative" and add this code snippet:

   ```python
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can access the employee directory. Please contact HR if you need this information."
        return {"response": response}
   ```

   This code checks if the user is authorized to access employee data, returning an error message if they're not.

   **Step 1.5**. Find the TODO comment: "4. If it's a guest user or someone else, ask for HR credentials" and add this code snippet:

   ```python
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to view this information. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}
   ```

   This code handles guest users by checking if they've provided the correct HR credentials in their request.

   **Step 1.6**. Find the TODO comment: "5. Load and format employee data" and add this code snippet:

   ```python
    try:
        employees_df = pd.read_csv("data/employees.csv")

        response = "## EMPLOYEE DIRECTORY\n\n"
        for _, emp in employees_df.iterrows():
            # Ensure we're handling the columns in the right order
            department = emp.get("department", "")
            role = emp.get("role", "")
            start_date = emp.get("start_date", "")

            # Format the display string properly
            response += f"• {emp['employee_id']}: {emp['name']} - {department}, {role} (Started: {start_date})\n"

        response += "\nThis information is confidential and should only be accessed by HR personnel."

    except Exception as e:
        response = f"An error occurred accessing employee data: {str(e)}"
   ```

   This code loads employee data from a CSV file and formats it into a readable directory listing.

   **Step 1.7**. Find the TODO comment: "6. Update memory with this interaction" and add this code snippet:

   ```python
    memory.update(state)
   ```

   This code updates the system's memory with the current interaction state.

   **Step 1.8**. Find the TODO comment: "7. Log the processing time" and add this code snippet:

   ```python
    log_processing_time("HR employee directory access", start_time)

    return {"response": response}
   ```

   This code logs how long the function took to execute and returns the formatted response.

2. **Implement the HR training records function.**

    **Step 2.1**. Find the TODO comment: "Implement the hr_training function to handle training records requests" and follow the steps below.
    
    **Step 2.2**. Find the TODO comment: "1. Initialize the start time for processing" and add this code snippet:
    
    ```python
    start_time = time.time()
    ```
    
    This code initializes a timer to track how long the function takes to execute.
    
    **Step 2.3**. Find the TODO comment: "2. Log the request" and add this code snippet:
    
    ```python
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "training_records"],
    )
    ```
    
    This code logs the user's request with diagnostic information for tracking purposes.
    
    **Step 2.4**. Find the TODO comment: "3. Check if user is Jane Doe (E002), the HR representative" and add this code snippet:
    
    ```python
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can access all training records. Please contact HR if you need this information."
        return {"response": response}
    ```
    
    This code checks if the user is authorized to access training records, returning an error message if they're not.
    
    **Step 2.5**. Find the TODO comment: "4. If it's a guest user or someone else, ask for HR credentials" and add this code snippet:
    
    ```python
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to view this information. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}
    ```
    
    This code handles guest users by checking if they've provided the correct HR credentials in their request.
    
    **Step 2.6**. Find the TODO comment: "5. Load and format training data" and add this code snippet:
    
    ```python
    try:
        training_df = pd.read_csv("data/training/master.csv")

        response = "## MASTER TRAINING RECORDS\n\n"

        # Group by employee and course
        training_df = training_df.sort_values(["employee_id", "course_id"])

        current_employee = None
        for _, record in training_df.iterrows():
            if current_employee != record["employee_id"]:
                current_employee = record["employee_id"]
                response += (
                    f"\n### {record['employee_name']} ({record['employee_id']})\n"
                )

            status = record["status"]
            completion = (
                record["completion_date"]
                if pd.notna(record["completion_date"])
                else "Not completed"
            )
            due = (
                f"Due: {record['due_date']}"
                if pd.notna(record["due_date"])
                else "No due date"
            )

            response += f"• {record['course_id']}: {status} ({completion}) - {due}\n"

        response += "\nThis information is confidential and should only be accessed by HR personnel."

    except Exception as e:
        response = f"An error occurred accessing training records: {str(e)}"
    ```
    
    This code loads training data from a CSV file, sorts it by employee and course, and formats it into a readable report.
    
    **Step 2.7**. Find the TODO comment: "6. Update memory with this interaction" and add this code snippet:
    
    ```python
    memory.update(state)
    ```
    
    This code updates the system's memory with the current interaction state.
    
    **Step 2.8**. Find the TODO comment: "7. Log the processing time" and add this code snippet:
    
    ```python
    log_processing_time("HR training records access", start_time)

    return {"response": response}
    ```
    
    This code logs how long the function took to execute and returns the formatted response.

3. **Implement the employee-specific training records function.**

    **Step 3.1**. Find the TODO comment: "Implement the hr_employee_training function to handle specific employee training requests" and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "1. Initialize the start time for processing" and add this code snippet:
    
    ```python
    start_time = time.time()
    ```
    
    This code initializes a timer to track how long the function takes to execute.
    
    **Step 3.3**. Find the TODO comment: "2. Log the request" and add this code snippet:
    
    ```python
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "employee_training"],
    )
    ```
    
    This code logs the user's request with diagnostic information for tracking purposes.
    
    **Step 3.4**. Find the TODO comment: "3. Check if user is Jane Doe (E002), the HR representative" and add this code snippet:
    
    ```python
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can access training records for other employees. Please contact HR if you need this information."
        return {"response": response}
    ```
    
    This code checks if the user is authorized to access employee training records, returning an error message if they're not.
    
    **Step 3.5**. Find the TODO comment: "4. If it's a guest user or someone else, ask for HR credentials" and add this code snippet:
    
    ```python
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to view this information. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}
    ```
    
    This code handles guest users by checking if they've provided the correct HR credentials in their request.
    
    **Step 3.6**. Find the TODO comment: "5. Try to extract employee name from the query" and add this code snippet:
    
    ```python
    query_lower = state.user_input.lower()
    employee_name = None
    ```
    
    This code prepares to extract an employee name from the user's query.
    
    **Step 3.7**. Find the TODO comment: "6. Check if the query contains an employee name" and add this code snippet:
    
    ```python
    try:
        employees_df = pd.read_csv("data/employees.csv")
        for _, emp in employees_df.iterrows():
            name_parts = emp["name"].lower().split()
            # Check if any part of the employee name is in the query
            for part in name_parts:
                if part in query_lower and len(part) > 2:  # Avoid matching common words
                    employee_name = emp["name"]
                    employee_id = emp["employee_id"]
                    break
            if employee_name:
                break

        if not employee_name:
            response = "I couldn't identify which employee's training records you want to view. Please specify the employee name clearly."
            return {"response": response}

        # Load and format training data for the specific employee
        training_df = pd.read_csv("data/training/master.csv")
        employee_records = training_df[training_df["employee_id"] == employee_id]

        if len(employee_records) == 0:
            response = f"No training records found for {employee_name}."
            return {"response": response}

        response = (
            f"## TRAINING RECORDS FOR {employee_name.upper()} ({employee_id})\n\n"
        )

        for _, record in employee_records.iterrows():
            status = record["status"]
            completion = (
                record["completion_date"]
                if pd.notna(record["completion_date"])
                else "Not completed"
            )
            due = (
                f"Due: {record['due_date']}"
                if pd.notna(record["due_date"])
                else "No due date"
            )

            response += f"• {record['course_id']}: {status} ({completion}) - {due}\n"

        response += "\nThis information is confidential and should only be accessed by HR personnel."

    except Exception as e:
        response = f"An error occurred accessing training records: {str(e)}"
    ```
    
    This code searches for an employee name in the query, then loads and formats that employee's training records.
    
    **Step 3.8**. Find the TODO comment: "7. Update memory with this interaction" and add this code snippet:
    
    ```python
    memory.update(state)
    ```
    
    This code updates the system's memory with the current interaction state.
    
    **Step 3.9**. Find the TODO comment: "8. Log the processing time" and add this code snippet:
    
    ```python
    log_processing_time("HR employee training access", start_time)

    return {"response": response}
    ```
    
    This code logs how long the function took to execute and returns the formatted response.

4. **Implement the employee update function.**

    **Step 4.1**. Find the TODO comment: "Implement the hr_update_employee function to handle employee updates" and follow the steps below.
    
    **Step 4.2**. Find the TODO comment: "1. Initialize the start time for processing" and add this code snippet:
    
    ```python
    start_time = time.time()
    ```
    
    This code initializes a timer to track how long the function takes to execute.
    
    **Step 4.3**. Find the TODO comment: "2. Log the request" and add this code snippet:
    
    ```python
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "employee_update"],
    )
    ```
    
    This code logs the user's request with diagnostic information for tracking purposes.
    
    **Step 4.4**. Find the TODO comment: "3. Check if the user is Jane Doe (E002), the HR representative" and add this code snippet:
    
    ```python
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can update employee information. Please contact HR if you need this functionality."
        return {"response": response}
    ```
    
    This code checks if the user is authorized to update employee information, returning an error message if they're not.
    
    **Step 4.5**. Find the TODO comment: "4. If it's a guest user or someone else, ask for HR credentials" and add this code snippet:
    
    ```python
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to use this functionality. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}
    ```
    
    This code handles guest users by checking if they've provided the correct HR credentials in their request.
    
    **Step 4.6**. Find the TODO comment: "5. Extract employee data from the intent" and add this code snippet:
    
    ```python
    if not state.intent.get("args"):
        response = (
            "No update information was provided. Please format your request with "
            "employee ID and the fields you want to update (name, department, role, or start_date)."
        )
        return {"response": response}

    args = state.intent["args"]
    employee_id = args.get("employee_id")

    if not employee_id:
        response = "No employee ID was provided. Please specify which employee you want to update."
        return {"response": response}
    ```
    
    This code extracts the employee ID and update information from the user's request.
    
    **Step 4.7**. Find the TODO comment: "6. Collect fields to update" and add this code snippet:
    
    ```python
    update_data = {}
    if args.get("name"):
        update_data["name"] = args["name"]
    if args.get("department"):
        update_data["department"] = args["department"]
    if args.get("role"):
        update_data["role"] = args["role"]
    if args.get("start_date"):
        update_data["start_date"] = args["start_date"]

    if not update_data:
        response = "No update fields were provided. Please specify what information you want to update."
        return {"response": response}

    # Update the employee
    employee_manager = EmployeeManager()
    result = employee_manager.update_employee(employee_id, update_data)
    ```
    
    This code collects the fields to update and calls the employee manager to perform the update.
    
    **Step 4.8**. Find the TODO comment: "7. Generate the response" and add this code snippet:
    
    ```python
    if result["success"]:
        response = f"## EMPLOYEE UPDATE SUCCESSFUL\n\n"
        response += f"Successfully updated employee {result['employee_id']}.\n\n"

        if "updated_data" in result:
            updated = result["updated_data"]
            response += "### Updated Information:\n"
            response += f"• Employee ID: {updated['employee_id']}\n"
            response += f"• Name: {updated['name']}\n"
            response += f"• Department: {updated['department']}\n"
            response += f"• Role: {updated['role']}\n"
            response += f"• Start Date: {updated['start_date']}\n"
    else:
        response = f"## EMPLOYEE UPDATE FAILED\n\n"
        response += f"{result['message']}"
    ```
    
    This code generates a response based on whether the update was successful.
    
    **Step 4.9**. Find the TODO comment: "8. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    memory.update(state)

    log_processing_time("HR employee update", start_time)

    return {"response": response}
    ```
    
    This code updates the system's memory, logs the processing time, and returns the response.

5. **Implement the bulk employee addition function.**

    **Step 5.1**. Find the TODO comment: "Implement the hr_bulk_add_employees function to handle bulk employee additions" and follow the steps below.
    
    **Step 5.2**. Find the TODO comment: "1. Initialize the start time for processing" and add this code snippet:
    
    ```python
    start_time = time.time()
    ```
    
    This code initializes a timer to track how long the function takes to execute.
    
    **Step 5.3**. Find the TODO comment: "2. Log the request" and add this code snippet:
    
    ```python
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "bulk_employee_add"],
    )
    ```
    
    This code logs the user's request with diagnostic information for tracking purposes.
    
    **Step 5.4**. Find the TODO comment: "3. Check if the user is Jane Doe (E002), the HR representative" and add this code snippet:
    
    ```python
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can add employees in bulk. Please contact HR if you need this functionality."
        return {"response": response}
    ```
    
    This code checks if the user is authorized to add employees in bulk, returning an error message if they're not.
    
    **Step 5.5**. Find the TODO comment: "4. Extract employee data from the intent" and add this code snippet:
    
    ```python
    if not state.intent.get("args") or not state.intent["args"].get("employees"):
        response = (
            "No employee data was provided. Please format your request with "
            "employee details including employee_id, name, department, and role for each employee."
        )
        return {"response": response}
    ```
    
    This code checks if the request includes employee data.
    
    **Step 5.6**. Find the TODO comment: "5. Collect employee data" and add this code snippet:
    
    ```python
    employee_manager = EmployeeManager()
    employees_data = state.intent["args"]["employees"]
    ```
    
    This code collects the employee data from the request.
    
    **Step 5.7**. Find the TODO comment: "6. Add employees in bulk" and add this code snippet:
    
    ```python
    result = employee_manager.add_employees_bulk(employees_data)
    ```
    
    This code calls the employee manager to add the employees in bulk.
    
    **Step 5.8**. Find the TODO comment: "7. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    memory.update(state)

    log_processing_time("HR bulk employee addition", start_time)

    return {"response": response}
    ```
    
    This code updates the system's memory, logs the processing time, and returns the response.

6. **Implement the HR analytics function.**

    **Step 6.1**. Find the TODO comment: "Implement the hr_analytics function to handle HR analytics requests" and follow the steps below.
    
    **Step 6.2**. Find the TODO comment: "1. Initialize the start time for processing and log the request" and add this code snippet:
    
    ```python
    start_time = time.time()
    
    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "analytics"],
    )
    ```
    
    This code initializes a timer and logs the user's request.
    
    **Step 6.3**. Find the TODO comment: "2. Check if the user is Jane Doe (E002), the HR representative" and add this code snippet:
    
    ```python
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can access analytics information. Please contact HR if you need this information."
        return {"response": response}
    ```
    
    This code checks if the user is authorized to access HR analytics, returning an error message if they're not.
    
    **Step 6.4**. Find the TODO comment: "3. Extract the query from the intent" and add this code snippet:
    
    ```python
    query = state.user_input.lower()
    ```
    
    This code extracts the query from the user's input.
    
    **Step 6.5**. Find the TODO comment: "4. Load employee and training data" and add this code snippet:
    
    ```python
    employees_df = pd.read_csv("data/employees.csv")
    training_df = pd.read_csv("data/training/master.csv")
    ```
    
    This code loads employee and training data from CSV files.
    
    **Step 6.6**. Find the TODO comment: "5. Training completion queries" and add this code snippet:
    
    ```python
    if "complete" in query or "finish" in query or "done" in query:
        if "hr-001" in query or "hr001" in query:
            # Get HR-001 completion statistics
            hr001_records = training_df[training_df["course_id"] == "HR-001"]
            completed = hr001_records[
                hr001_records["status"].isin(["Completed"])
            ].shape[0]
            total = hr001_records.shape[0]
            not_completed = total - completed
    
            response = f"## HR-001 Course Completion Analysis\n\n"
            response += f"• Total Enrollments: {total}\n"
            response += f"• Completed: {completed} ({completed/total*100:.1f}%)\n"
            response += f"• Not Completed: {not_completed} ({not_completed/total*100:.1f}%)\n\n"
    
            # Add details of employees who haven't completed
            if "who" in query or "which" in query or "list" in query:
                incomplete_records = hr001_records[
                    ~hr001_records["status"].isin(["Completed"])
                ]
                response += "### Employees Who Haven't Completed HR-001:\n"
                for _, record in incomplete_records.iterrows():
                    status = record["status"]
                    response += f"• {record['employee_name']} ({record['employee_id']}): {status}\n"
    
        elif "hr-002" in query or "hr002" in query:
            # Get HR-002 completion statistics
            hr002_records = training_df[training_df["course_id"] == "HR-002"]
            completed = hr002_records[
                hr002_records["status"].isin(["Completed"])
            ].shape[0]
            total = hr002_records.shape[0]
            not_completed = total - completed
    
            response = f"## HR-002 Course Completion Analysis\n\n"
            response += f"• Total Enrollments: {total}\n"
            response += f"• Completed: {completed} ({completed/total*100:.1f}%)\n"
            response += f"• Not Completed: {not_completed} ({not_completed/total*100:.1f}%)\n\n"
    
            # Add details of employees who haven't completed
            if "who" in query or "which" in query or "list" in query:
                incomplete_records = hr002_records[
                    ~hr002_records["status"].isin(["Completed"])
                ]
                response += "### Employees Who Haven't Completed HR-002:\n"
                for _, record in incomplete_records.iterrows():
                    status = record["status"]
                    response += f"• {record['employee_name']} ({record['employee_id']}): {status}\n"
    
        elif "sec-010" in query or "sec010" in query:
            # Get SEC-010 completion statistics
            sec010_records = training_df[training_df["course_id"] == "SEC-010"]
            completed = sec010_records[
                sec010_records["status"].isin(["Completed"])
            ].shape[0]
            total = sec010_records.shape[0]
            not_completed = total - completed
    
            response = f"## SEC-010 Course Completion Analysis\n\n"
            response += f"• Total Enrollments: {total}\n"
            response += f"• Completed: {completed} ({completed/total*100:.1f}%)\n"
            response += f"• Not Completed: {not_completed} ({not_completed/total*100:.1f}%)\n\n"
    
            # Add details of employees who haven't completed
            if "who" in query or "which" in query or "list" in query:
                incomplete_records = sec010_records[
                    ~sec010_records["status"].isin(["Completed"])
                ]
                response += "### Employees Who Haven't Completed SEC-010:\n"
                for _, record in incomplete_records.iterrows():
                    status = record["status"]
                    response += f"• {record['employee_name']} ({record['employee_id']}): {status}\n"
    
        else:
            # General completion statistics for all courses
            course_stats = {}
            for course_id in training_df["course_id"].unique():
                course_records = training_df[training_df["course_id"] == course_id]
                completed = course_records[
                    course_records["status"].isin(["Completed"])
                ].shape[0]
                total = course_records.shape[0]
                not_completed = total - completed
                course_stats[course_id] = {
                    "total": total,
                    "completed": completed,
                    "not_completed": not_completed,
                    "completion_rate": (
                        (completed / total * 100) if total > 0 else 0
                    ),
                }
    
            response = f"## Training Completion Analysis\n\n"
    
            # Sort courses by completion rate
            sorted_courses = sorted(
                course_stats.items(), key=lambda x: x[1]["completion_rate"]
            )
    
            for course_id, stats in sorted_courses:
                response += f"### {course_id}:\n"
                response += f"• Total Enrollments: {stats['total']}\n"
                response += f"• Completed: {stats['completed']} ({stats['completion_rate']:.1f}%)\n"
                response += f"• Not Completed: {stats['not_completed']} ({100-stats['completion_rate']:.1f}%)\n\n"
    ```
    
    This code handles queries about training completion, providing statistics for specific courses or all courses.
    
    **Step 6.7**. Find the TODO comment: "6. Department statistics" and add this code snippet:
    
    ```python
    elif "department" in query:
        # Get department statistics
        dept_counts = employees_df["department"].value_counts()
        total_employees = employees_df.shape[0]
    
        response = f"## Department Analysis\n\n"
        response += f"Total Employees: {total_employees}\n\n"
    
        for dept, count in dept_counts.items():
            if pd.notna(dept) and dept:  # Ensure department is not empty
                percentage = (count / total_employees) * 100
                response += f"• {dept}: {count} employees ({percentage:.1f}%)\n"
    
        # Add training completion by department if relevant
        if "training" in query or "course" in query or "complete" in query:
            response += "\n### Training Completion by Department\n\n"
    
            for dept in dept_counts.index:
                if pd.notna(dept) and dept:  # Ensure department is not empty
                    dept_employees = employees_df[
                        employees_df["department"] == dept
                    ]["employee_id"].tolist()
                    dept_records = training_df[
                        training_df["employee_id"].isin(dept_employees)
                    ]
    
                    if not dept_records.empty:
                        completed = dept_records[
                            dept_records["status"] == "Completed"
                        ].shape[0]
                        total = dept_records.shape[0]
                        completion_rate = (
                            (completed / total) * 100 if total > 0 else 0
                        )
    
                        response += f"**{dept}**:\n"
                        response += f"• Course Enrollments: {total}\n"
                        response += (
                            f"• Completed: {completed} ({completion_rate:.1f}%)\n\n"
                        )
    ```
    
    This code handles queries about department statistics, providing employee counts and training completion rates by department.
    
    **Step 6.8**. Find the TODO comment: "7. New employee statistics" and add this code snippet:
    
    ```python
    elif "new" in query and "employee" in query:
        # Define new employees as those who started within the last 30 days
        today = pd.Timestamp(datetime.now().date())
        cutoff_date = (today - pd.Timedelta(days=30)).strftime("%Y-%m-%d")
    
        new_employees = employees_df[employees_df["start_date"] >= cutoff_date]
        count_new = new_employees.shape[0]
    
        response = f"## New Employee Analysis\n\n"
        response += f"Total new employees (last 30 days): {count_new}\n\n"
    
        if count_new > 0:
            response += "### New Employees:\n"
            for _, emp in new_employees.iterrows():
                response += f"• {emp['name']} ({emp['employee_id']}) - {emp['department']}, {emp['role']} (Started: {emp['start_date']})\n"
    
            # Add training enrollment status for new employees
            if "training" in query or "course" in query:
                response += "\n### Training Status for New Employees\n\n"
    
                new_emp_ids = new_employees["employee_id"].tolist()
                for emp_id in new_emp_ids:
                    emp_name = new_employees[
                        new_employees["employee_id"] == emp_id
                    ]["name"].iloc[0]
                    response += f"**{emp_name} ({emp_id})**:\n"
    
                    emp_records = training_df[training_df["employee_id"] == emp_id]
                    if emp_records.empty:
                        response += "• No training courses enrolled\n\n"
                    else:
                        for _, record in emp_records.iterrows():
                            status = record["status"]
                            course = record["course_id"]
                            response += f"• {course}: {status}\n"
                        response += "\n"
    ```
    
    This code handles queries about new employees, providing information about employees who started within the last 30 days.
    
    **Step 6.9**. Find the TODO comment: "8. Default response for unrecognized analytics queries" and add this code snippet:
    
    ```python
    else:
        response = (
            "I'm not sure what analytics you're looking for. You can ask about:\n\n"
            "• Course completion rates (e.g., 'How many people have completed HR-001?')\n"
            "• Department statistics (e.g., 'Show me department breakdown')\n"
            "• New employee information (e.g., 'How many new employees do we have?')\n"
            "• Training enrollment by department (e.g., 'What's the training status by department?')\n"
        )
    ```
    
    This code provides a helpful message when the system doesn't recognize the analytics query.
    
    **Step 6.10**. Find the TODO comment: "9. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    # Update memory with this interaction
    memory.update(state)
    
    log_processing_time("HR analytics", start_time)
    
    return {"response": response}
    ```
    
    This code updates the system's memory, logs the processing time, and returns the response.



### Task 10: Implement Training-Related Nodes

The `training_nodes.py` file contains implementations for several training-related nodes that handle training records, course enrollments, and completions. 

The TODO tasks involve implementing five key functions: `training_lookup` (viewing employee training records), `training_courses` (listing available courses), `training_enroll` (handling course enrollment), `training_update` (marking course completion), and `mandatory_training` (enrolling in all mandatory courses).

The `training_lookup` function retrieves and generates training record snapshots. `training_courses` loads and optionally filters the course catalog while providing enrollment instructions. `training_enroll` processes single or batch course enrollments. `training_update` marks courses as completed, supporting both individual and batch updates. `mandatory_training` enrolls employees in all required courses.

Each function follows a pattern: starting a timer, logging the request, processing the training task, generating a formatted response, updating memory, and logging processing time. These nodes enable employees to view, enroll in, and complete training courses.

1. **Locate the `training_lookup` function in the `training_nodes.py` file.**

    **Step 1.1**. Find the TODO comment: "Implement the training_lookup function to handle training record lookups" and follow the steps below.
    
    **Step 1.2**. Find the TODO comment: "1. Initialize the start time for processing and log the request" and add this code snippet:
    
    ```python
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=(state.previous_question is not None),
        detected_entities=["training_records"],
    )
    ```
    
    This code initializes a timer to track processing time and logs the user's request with diagnostic information.
    
    **Step 1.3**. Find the TODO comment: "2. Get employee records and generate a snapshot" and add this code snippet:
    
    ```python
    # Get employee records
    employee_records = training_records.get_employee_record(state.employee_id)
    snapshot_path = training_records.create_snapshot(state.employee_id)

    # Generate the response
    response = f"Here's your current training record:\n\n"
    if len(employee_records) == 0:
        response += "You are not currently enrolled in any training courses."
    else:
        for _, record in employee_records.iterrows():
            status = record["status"]
            course = f"{record['course_id']}: {record['course_name']}"

            # Format enrollment date if available
            enrolled = ""
            if "enrolled_date" in record and pd.notna(record["enrolled_date"]):
                enrolled = f"Enrolled: {record['enrolled_date']}"

            # Format completion date
            completion = (
                record["completion_date"]
                if pd.notna(record["completion_date"])
                else "Not completed"
            )

            # Format due date
            due = (
                f"Due: {record['due_date']}"
                if pd.notna(record["due_date"])
                else "No due date"
            )

            # Include enrollment date in the display
            if enrolled:
                response += (
                    f"• {course} - {status} ({enrolled}, {completion}) - {due}\n"
                )
            else:
                response += f"• {course} - {status} ({completion}) - {due}\n"

    response += (
        f"\nA snapshot of your training record has been saved to {snapshot_path}."
    )
    ```
    
    This code retrieves the employee's training records, creates a snapshot file, and formats a detailed response showing each course with its status, enrollment date, completion status, and due date.
    
    **Step 1.4**. Find the TODO comment: "3. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Training lookup", start_time)

    return {"response": response}
    ```
    
    This code updates the assistant's memory with the current interaction and logs how long the processing took before returning the response.

2. **Locate the `training_courses` function in the `training_nodes.py` file.**

    **Step 2.1**. Find the TODO comment: "Implement the training_courses function to handle training course lookups" and follow the steps below.
    
    **Step 2.2**. Find the TODO comment: "1. Initialize the start time for processing and log the request" and add this code snippet:
    
    ```python
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=(state.previous_question is not None),
        detected_entities=["course_catalog"],
    )
    ```
    
    This code initializes a timer and logs the request with appropriate diagnostic information.
    
    **Step 2.3**. Find the TODO comment: "2. Load courses from catalog and check if we need to filter by category" and add this code snippet:
    
    ```python
    # Load courses from catalog
    courses_df = training_records.load_courses()

    # Check if we need to filter by category
    category = None
    query_lower = state.user_input.lower()
    if "mandatory" in query_lower or "required" in query_lower:
        category = "Mandatory"
        filtered_courses = training_records.get_available_courses(category=category)
        response = "Here are the mandatory/required courses:\n\n"
    elif "elective" in query_lower or "optional" in query_lower:
        category = "Elective"
        filtered_courses = training_records.get_available_courses(category=category)
        response = "Here are the elective/optional courses:\n\n"
    else:
        filtered_courses = courses_df
        response = "Here are all available training courses:\n\n"
    ```
    
    This code loads all courses from the catalog and checks if the user's query contains keywords like "mandatory" or "elective" to filter the courses accordingly.
    
    **Step 2.4**. Find the TODO comment: "3. Generate response, add instructions for enrollment, and check compliance status" and add this code snippet:
    
    ```python
    # Generate response
    if len(filtered_courses) == 0:
        response = "No courses are currently available in the catalog."
    else:
        # Group by category if not already filtered
        if category is None:
            # First list mandatory courses
            mandatory = training_records.get_available_courses(category="Mandatory")
            if len(mandatory) > 0:
                response += "🛡️ MANDATORY COURSES (required):\n"
                for _, course in mandatory.iterrows():
                    renewal = (
                        f" (Renewal: {course['renewal_period']})"
                        if pd.notna(course["renewal_period"])
                        else ""
                    )
                    response += (
                        f"• {course['course_code']}: {course['title']}{renewal}\n"
                    )
                response += "\n"

            # Then list elective courses
            elective = training_records.get_available_courses(category="Elective")
            if len(elective) > 0:
                response += "📚 ELECTIVE COURSES (optional):\n"
                for _, course in elective.iterrows():
                    response += f"• {course['course_code']}: {course['title']}\n"

        else:
            # List courses in the filtered category
            for _, course in filtered_courses.iterrows():
                if category == "Mandatory":
                    renewal = (
                        f" (Renewal: {course['renewal_period']})"
                        if pd.notna(course["renewal_period"])
                        else ""
                    )
                    response += (
                        f"• {course['course_code']}: {course['title']}{renewal}\n"
                    )
                else:
                    response += f"• {course['course_code']}: {course['title']}\n"

    # Add instructions for enrollment
    response += "\nTo enroll in a course, say 'Enroll me in [COURSE CODE]'"

    # Add information about compliance if applicable
    if category == "Mandatory" or category is None:
        response += "\nTo check your compliance status, say 'Am I compliant with mandatory training?'"
    ```
    
    This code formats the response to display available courses, grouped by category if needed, and adds helpful instructions for enrollment and compliance checking.
    
    **Step 2.5**. Find the TODO comment: "4. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Training courses lookup", start_time)

    return {"response": response}
    ```
    
    This code updates the assistant's memory with the current interaction, logs the processing time, and returns the formatted response.

3. **Locate the `training_enroll` function in the `training_nodes.py` file.**

    **Step 3.1**. Find the TODO comment: "Implement the training_enroll function to handle training course enrollments" and follow the steps below.
    
    **Step 3.2**. Find the TODO comment: "1. Initialize the start time for processing" and add this code snippet:
    
    ```python
    start_time = time.time()
    ```
    
    This code initializes a timer to track how long the enrollment process takes.
    
    **Step 3.3**. Find the TODO comment: "2. Get course IDs from intent args, ensuring it's a list, and log the request" and add this code snippet:
    
    ```python
    # Get course IDs from intent args
    course_ids = state.intent["args"].get("course_ids", [])

    # Ensure we always have a list, even if only one course ID was provided
    if not isinstance(course_ids, list):
        course_ids = [course_ids]

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=[
            "course_enrollment",
            f"course_ids:{','.join(course_ids)}",
        ],
    )
    ```
    
    This code extracts course IDs from the intent arguments, ensures they're in a list format, and logs the enrollment request with diagnostic information.
    
    **Step 3.4**. Find the TODO comment: "3. Process each course ID" and add this code snippet:
    
    ```python
    # Process each course ID
    results = []
    for course_id in course_ids:
        # In a real system, we'd look up the course name from a course catalog
        course_name = f"Course {course_id}"

        success, message = training_records.enroll_in_course(
            state.employee_id, course_id, course_name
        )
        results.append((course_id, success, message))
    ```
    
    This code processes each course ID by attempting to enroll the employee in the course and storing the results for later response generation.
    
    **Step 3.5**. Find the TODO comment: "4. Generate the response based on the results" and add this code snippet:
    
    ```python
    # Generate the response based on the results
    if len(results) == 1:
        # Single course enrollment
        course_id, success, message = results[0]
        if success:
            response = f"You've been successfully enrolled in {course_id}."
        else:
            response = f"Enrollment failed for {course_id}: {message}"
    else:
        # Multiple course enrollments
        response = "I've processed your course enrollments:\n\n"
        success_count = 0
        for course_id, success, message in results:
            if success:
                response += f"• {course_id}: Successfully enrolled\n"
                success_count += 1
            else:
                response += f"• {course_id}: Failed - {message}\n"

        if success_count == len(results):
            response = (
                f"You've been successfully enrolled in all {len(results)} courses:\n\n"
                + "\n".join([f"• {r[0]}" for r in results])
            )
        elif success_count == 0:
            response = (
                "I was unable to enroll you in any of the courses:\n\n"
                + "\n".join([f"• {r[0]}: {r[2]}" for r in results])
            )
    ```
    
    This code generates a response based on the enrollment results, handling both single and multiple course enrollments with appropriate success and failure messages.
    
    **Step 3.6**. Find the TODO comment: "5. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Training enrollment", start_time)

    return {"response": response}
    ```
    
    This code updates the assistant's memory with the current interaction, logs the processing time, and returns the response.

4. **Locate the `training_update` function in the `training_nodes.py` file.**

    **Step 4.1**. Find the TODO comment: "Implement the training_update function to handle training course completions" and follow the steps below.
    
    **Step 4.2**. Find the TODO comment: "1. Initialize the start time for processing, get course IDs from intent args" and add this code snippet:
    
    ```python
    start_time = time.time()

    # Get course IDs from intent args
    course_ids = state.intent["args"].get("course_ids", [])

    # Ensure we always have a list, even if only one course ID was provided
    if not isinstance(course_ids, list):
        course_ids = [course_ids]
    ```
    
    This code initializes a timer and extracts course IDs from the intent arguments, ensuring they're in a list format.
    
    **Step 4.3**. Find the TODO comment: "2. Log the request" and add this code snippet:
    
    ```python
    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=[
            "course_completion",
            f"course_ids:{','.join(course_ids)}",
        ],
    )
    ```
    
    This code logs the course completion request with appropriate diagnostic information.
    
    **Step 4.4**. Find the TODO comment: "3. Process each course ID and generate a response" and add this code snippet:
    
    ```python
    # Process each course ID
    results = []
    for course_id in course_ids:
        success, message = training_records.update_completion(
            state.employee_id, course_id
        )
        results.append((course_id, success, message))

    # Generate the response based on the results
    if len(results) == 1:
        # Single course update
        course_id, success, message = results[0]
        if success:
            response = f"Great job! I've marked {course_id} as completed."
        else:
            response = f"Update failed for {course_id}: {message}"
    else:
        # Multiple course updates
        response = "I've processed your course completions:\n\n"
        success_count = 0
        for course_id, success, message in results:
            if success:
                response += f"• {course_id}: Successfully marked as completed\n"
                success_count += 1
            else:
                response += f"• {course_id}: Failed - {message}\n"

        if success_count == len(results):
            response = (
                f"Great job! I've marked all {len(results)} courses as completed:\n\n"
                + "\n".join([f"• {r[0]}" for r in results])
            )
        elif success_count == 0:
            response = "I was unable to update any of the courses:\n\n" + "\n".join(
                [f"• {r[0]}: {r[2]}" for r in results]
            )
    ```
    
    This code processes each course ID by marking it as completed and generates a response based on the results, handling both single and multiple course completions.
    
    **Step 4.5**. Find the TODO comment: "4. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Training update", start_time)

    return {"response": response}
    ```
    
    This code updates the assistant's memory with the current interaction, logs the processing time, and returns the response.

5. **Locate the `mandatory_training` function in the `training_nodes.py` file.**

    **Step 5.1**. Find the TODO comment: "Implement the mandatory_training function to handle mandatory training enrollments" and follow the steps below.
    
    **Step 5.2**. Find the TODO comment: "1. Initialize the start time for processing and log the request" and add this code snippet:
    
    ```python
    start_time = time.time()
    
    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["mandatory_training", "batch_enrollment"],
    )
    ```
    
    This code initializes a timer and logs the mandatory training enrollment request with appropriate diagnostic information.
    
    **Step 5.3**. Find the TODO comment: "2. Process mandatory enrollments and generate a response" and add this code snippet:
    
    ```python
    # Process mandatory enrollments
    results = training_records.enroll_mandatory_courses(state.employee_id)
    
    # Generate response
    response = "I've processed your mandatory training enrollment:\n\n"
    for course_id, success, message in results:
        if success:
            response += f"• Enrolled in {course_id}\n"
        else:
            response += f"• {course_id}: {message}\n"
    ```
    
    This code enrolls the employee in all mandatory courses and generates a response listing the enrollment results for each course.
    
    **Step 5.4**. Find the TODO comment: "3. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    # Update memory with this interaction
    memory.update(state)
    
    log_processing_time("Mandatory training enrollment", start_time)
    
    return {"response": response}
    ```
    
    This code updates the assistant's memory with the current interaction, logs the processing time, and returns the response.



### Task 11: Implement Fallback Utility Nodes

The `utility_nodes.py` file contains utility nodes for the HR assistant orchestration graph, with the primary TODO task being the implementation of the `fallback` function. 

This function handles unrecognized requests as a catch-all. It starts a timer, logs the fallback request, and generates a friendly message explaining that the assistant only helps with HR-related questions. It suggests asking about policies, benefits, or training, and mentions typing 'help' for capabilities. The function updates conversation memory, logs processing time, and returns the response. This fallback node provides a graceful experience when encountering queries outside the system's domain, guiding users back to supported topics rather than failing to respond appropriately. It's essential for handling edge cases and keeping conversations productive when users ask about topics beyond the assistant's capabilities.

11. **Locate the `fallback` function in the `utility_nodes.py` file.**

    **Step 11.1**. Find the TODO comment: "Implement the fallback function to handle unrecognized intents" and follow the steps below.
    
    **Step 11.2**. Find the TODO comment: "1. Initialize the start time for processing and log the request" and add this code snippet:
    
    ```python
    start_time = time.time()
    
    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["fallback"],
    )
    ```
    
    This code initializes a timer to track processing time and logs the user's query that couldn't be matched to any intent, marking it as a fallback case.
    
    **Step 11.3**. Find the TODO comment: "2. Generate the fallback response" and add this code snippet:
    
    ```python
    response = (
        "I'm sorry, I can only help with HR-related questions and tasks. "
        "I can assist with policies, benefits, or training - what would you like to know? "
        "Type 'help' to see what I can do."
    )
    ```
    
    This code creates a friendly response that explains the assistant's limitations, suggests topics the user can ask about, and provides a hint about using the 'help' command.
    
    **Step 11.4**. Find the TODO comment: "3. Update memory with this interaction and log the processing time" and add this code snippet:
    
    ```python
    memory.update(state)
    
    log_processing_time("Fallback", start_time)
    
    return {"response": response}
    ```
    
    This code updates the conversation memory with the current interaction, logs how long it took to process the fallback response, and returns the response to be shown to the user.



### Task 12: Implement Document Loader

The `document_loader.py` file is responsible for loading, processing, and vectorizing HR policy and benefits documents for retrieval. 

The main TODO task is implementing `load_documents`, which loads and processes policy and benefits documents for retrieval. The implementation must verify directories exist, create document loaders with error handling for different file types, and load documents from both directories. It must tag documents with source information and metadata, including document type classification based on filename keywords (identifying leave policies, workplace policies, health benefits, etc.).

The function needs to split documents into chunks with optimized parameters, balancing chunk size and overlap to maintain context while enabling precise retrieval. Additional tasks include implementing `create_vector_store` to create and save a FAISS vector store from document chunks, and `load_vector_store` to load existing vector stores with proper error handling. These functions form the RAG system foundation, enabling relevant document retrieval when answering employee questions.

12. **Implement the Document Loader in `document_loader.py`.**

    **Step 12.1**. Find the TODO comment: "Implement the load_documents function to load and process documents" and follow the steps below.
    
    **Step 12.2**. Find the TODO comment: "1. Ensure the directories exist" and add this code snippet:
    
    ```python
    # Ensure directories exist
    os.makedirs(policy_dir, exist_ok=True)
    os.makedirs(benefits_dir, exist_ok=True)
    ```
    
    This code creates the policy and benefits directories if they don't already exist.
    
    **Step 12.3**. Find the TODO comment: "2. Create loaders with improved error handling" and add this code snippet:
    
    ```python
    # Create loaders with improved error handling
    policy_loader = DirectoryLoader(
        policy_dir,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
            "autodetect_encoding": True,
        },
    )
    benefits_loader = DirectoryLoader(
        benefits_dir,
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={
            "encoding": "utf-8",
            "autodetect_encoding": True,
        },
    )
    ```
    
    This code creates directory loaders for both policy and benefits directories, configuring them to load text files with proper encoding detection.
    
    **Step 12.4**. Find the TODO comment: "3. Load documents with better error handling" and add this code snippet:
    
    ```python
    # Load documents with better error handling
    try:
        policy_docs = policy_loader.load()
        print(f"Loaded {len(policy_docs)} policy documents from {policy_dir}")
    except Exception as e:
        print(f"Error loading policy documents: {e}")
        policy_docs = []
    
    try:
        benefits_docs = benefits_loader.load()
        print(f"Loaded {len(benefits_docs)} benefit documents from {benefits_dir}")
    except Exception as e:
        print(f"Error loading benefit documents: {e}")
        benefits_docs = []
    ```
    
    This code loads documents from both directories with error handling, ensuring the program continues even if some documents can't be loaded.
    
    **Step 12.5**. Find the TODO comment: "4. Tag documents with source and proper file names" and add this code snippet:
    
    ```python
    # Tag documents with source and proper file names
    for doc in policy_docs:
        source_path = doc.metadata.get("source", "")
        doc.metadata["source"] = "policy"
        doc.metadata["source_file"] = os.path.basename(source_path)
        doc.metadata["full_source_path"] = source_path
        # Add document type based on filename keywords for better classification
        filename = os.path.basename(source_path).lower()
        if any(
            keyword in filename for keyword in ["pto", "vacation", "time off", "leave"]
        ):
            doc.metadata["document_type"] = "leave_policy"
        elif any(
            keyword in filename
            for keyword in ["harassment", "discrimination", "conduct"]
        ):
            doc.metadata["document_type"] = "workplace_policy"
        else:
            doc.metadata["document_type"] = "general_policy"
    
    for doc in benefits_docs:
        source_path = doc.metadata.get("source", "")
        doc.metadata["source"] = "benefit"
        doc.metadata["source_file"] = os.path.basename(source_path)
        doc.metadata["full_source_path"] = source_path
        # Add benefit type based on filename keywords
        filename = os.path.basename(source_path).lower()
        if any(
            keyword in filename for keyword in ["health", "medical", "dental", "vision"]
        ):
            doc.metadata["document_type"] = "health_benefits"
        elif any(keyword in filename for keyword in ["retirement", "401k", "pension"]):
            doc.metadata["document_type"] = "retirement_benefits"
        else:
            doc.metadata["document_type"] = "general_benefits"
    ```
    
    This code adds metadata to each document, including source information and document type classification based on filename keywords.
    
    **Step 12.6**. Find the TODO comment: "5. Combine documents and split into chunks" and add this code snippet:
    
    ```python
    # Combine documents
    all_docs = policy_docs + benefits_docs
    
    if not all_docs:
        print("Warning: No documents were loaded. Check the data directories.")
        return []
    
    # Split documents with improved settings for better context retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""],
        keep_separator=True,
    )
    chunks = text_splitter.split_documents(all_docs)
    
    print(f"Created {len(chunks)} document chunks from {len(all_docs)} documents")
    return chunks
    ```
    
    This code combines all documents, checks if any were loaded, splits them into chunks with optimized parameters, and returns the chunks.
    
    **Step 12.7**. Find the TODO comment: "Implement the create_vector_store function to create and save the vector store" and follow the steps below.
    
    **Step 12.8**. Find the TODO comment: "1. Check if chunks are provided and ensure the directory exists" and add this code snippet:
    
    ```python
    if not chunks:
        print("No document chunks provided to create vector store.")
        return None
    
    # Ensure vector store directory exists
    os.makedirs(vector_store_path, exist_ok=True)
    ```
    
    This code checks if document chunks were provided and creates the vector store directory if it doesn't exist.
    
    **Step 12.9**. Find the TODO comment: "2. Create the FAISS vector store with improved error handling" and add this code snippet:
    
    ```python
    # Use sentence-transformers for embeddings (offline use)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    try:
        print(f"Creating vector store with {len(chunks)} chunks...")
        vector_store = FAISS.from_documents(chunks, embeddings)
        vector_store.save_local(vector_store_path)
        print(f"Vector store saved to {vector_store_path}")
        return vector_store
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None
    ```
    
    This code creates a FAISS vector store from the document chunks using HuggingFace embeddings, saves it to the specified path, and handles any errors that occur.
    
    **Step 12.10**. Find the TODO comment: "Implement the load_vector_store function to load an existing vector store" and follow the steps below.
    
    **Step 12.11**. Find the TODO comment: "1. Check if the vector store path exists and load it with improved error handling" and add this code snippet:
    
    ```python
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists(vector_store_path):
        try:
            print(f"Loading vector store from {vector_store_path}...")
            return FAISS.load_local(
                vector_store_path, embeddings, allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Error loading vector store: {e}")
            raise FileNotFoundError(
                f"Failed to load vector store from {vector_store_path}: {e}"
            )
    else:
        raise FileNotFoundError(f"Vector store not found at {vector_store_path}")
    ```
    
    This code checks if the vector store path exists, loads the vector store with proper error handling, and raises appropriate exceptions if the vector store can't be loaded.



## Task 13: Implement `BenefitsRAG` Class

The `benefits_qa.py` file contains the `BenefitsRAG` class, which handles benefits-related queries using retrieval-augmented generation. 

The TODO tasks involve implementing key methods for this class:

The constructor initializes the vector store, builds a benefit file cache, and sets up specialized prompt templates. `_build_benefit_cache` reads benefit files and creates content hashes for partial matching. `find_document_source` identifies source documents for retrieved content using multiple techniques.

`is_sensitive_topic` detects queries about sensitive topics like mental health. `is_comparative_question` and `is_relationship_question` identify queries comparing benefits or asking about benefit relationships. `is_followup_question` detects follow-up queries.

`expand_query` enhances queries with related terms to improve retrieval. `extract_entities_for_comparison` identifies benefit entities in comparative queries. `get_relevant_documents` retrieves documents with special handling for comparative and sensitive topics. `generate_response` creates responses using appropriate prompt templates based on query type.

This class ensures accurate, contextually appropriate responses to benefit questions.

13. **Implement the `BenefitsRAG` Class in the `benefits_qa.py` file.**

    **Step 13.1**. Find the TODO comment: "Implement the BenefitsRAG class to handle benefits-related queries" and follow the steps below.
    
    **Step 13.2**. Find the TODO comment: "1. Define the class constructor, initialize the vector store, and build the benefit cache" and add this code snippet:
    
    ```python
    def __init__(self, llm, vector_store_path="data/vector_store"):
        """Initialize the Benefits RAG component"""
        self.llm = llm
        try:
            self.vector_store = load_vector_store(vector_store_path)
        except FileNotFoundError:
            # If vector store doesn't exist yet, we'll initialize with empty retriever
            # It will be populated later during setup
            self.vector_store = None
    
        # Build a content cache of benefit files for better matching
        self.benefit_files = {}
        self.benefit_content_hashes = {}
        self._build_benefit_cache()
    ```
    
    This code initializes the BenefitsRAG class with a language model, loads the vector store from the specified path, and builds a cache of benefit files for better matching.
    
    **Step 13.3**. Find the TODO comment: "2. Standard QA prompt for general benefit questions" and add this code snippet:
    
    ```python
    self.qa_prompt = ChatPromptTemplate.from_template(
        """
    You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about employee benefits.
    
    Use ONLY the following context to answer the question. If you don't have enough information based on the context, say 
    "I don't have enough information about that in my knowledge base. Please contact HR for more details."
    
    Context:
    {context}
    
    Question: {question}
    
    Answer the question based only on the provided context. Include the source document name in your response 
    for citation purposes. Format your response in a friendly, helpful tone.
    
    When answering follow-up questions or comparing policies, make sure to use all relevant context provided.
    If the question asks for a comparison between different benefits or policies, make sure
    to address all relevant aspects in your answer with clear distinctions between them.
    
    If multiple benefits are mentioned in the question, be sure to discuss each one and highlight the key 
    similarities and differences between them. Structure your answer clearly, using bullet points where appropriate.
    """
    )
    ```
    
    This code defines a prompt template for general benefit questions that instructs the AI to answer based only on the provided context and include source document names for citation.
    
    **Step 13.4**. Find the TODO comment: "3. Specialized prompt for sensitive topics like mental health, disabilities, etc." and add this code snippet:
    
    ```python
    self.sensitive_topic_prompt = ChatPromptTemplate.from_template(
        """
    You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about employee benefits,
    including sensitive topics like mental health resources, disability accommodations, or wellness programs.
    
    Use the following context to answer the question.
    
    Context:
    {context}
    
    Question: {question}
    
    Important instructions for sensitive topics:
    1. Present information about support resources and company assistance programs first
    2. Explain the benefits' protection and confidentiality provisions clearly
    3. Describe eligibility and enrollment processes in clear terms
    4. Use compassionate, non-judgmental language throughout your response
    5. Emphasize that seeking help is encouraged and supported
    6. Include the source document name for citation
    
    For substance abuse, addiction, or mental health questions specifically:
    7. Always mention Employee Assistance Program (EAP) resources if available in the context
    8. Discuss both the Wellness Program and related policies together if relevant
    9. Emphasize confidentiality and non-punitive aspects of seeking help
    10. Synthesize information from multiple documents to provide a complete answer
    11. Address how different benefits and programs work together to support employees
    
    If the context doesn't specifically address the question (for example, if the Wellness Program doesn't 
    explicitly mention addiction):
    12. Acknowledge this limitation clearly: "Based on the available information, our [specific policy] documentation 
       doesn't explicitly mention [topic]. However, I can share what our policies do cover:"
    13. Provide the most relevant information you do have (e.g., smoking cessation programs, EAP resources, etc.)
    14. Offer to search across all policies: "Would you like me to search all company policies for information about [topic]?"
    15. Recommend contacting HR for more specific information
    16. Do NOT respond with only "I don't have enough information" - always try to provide some helpful direction
    
    Answer the question based on the provided context. Format your response in a friendly, supportive tone.
    """
    )
    ```
    
    This code defines a specialized prompt template for sensitive topics that provides detailed instructions on how to handle questions about mental health, disabilities, and other sensitive topics with compassion and thoroughness.
    
    **Step 13.5**. Find the TODO comment: "4. Specialized prompt for comparative questions" and add this code snippet:
    
    ```python
    self.comparison_prompt = ChatPromptTemplate.from_template(
        """
    You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer questions about employee benefits.
    
    The user has asked a comparative question about different benefits. Use ONLY the following context to answer the question.
    If you don't have enough information, say "I don't have enough information about that in my knowledge base. Please contact HR for more details."
    
    Context:
    {context}
    
    Question: {question}
    
    In your answer:
    17. Address each benefit mentioned in the question separately first
    18. Then provide a clear comparison highlighting key similarities and differences
    19. Use bullet points for clarity when listing features of each benefit
    20. Include the source document names for citation purposes
    21. Format your response in a friendly, helpful tone
    
    IMPORTANT: When answering questions about relationships between benefits or policies (e.g., "Does maternity leave count as PTO?", "Is X part of Y?", "Does X affect Y?"):
    22. Begin your answer with a direct, explicit statement about the relationship (e.g., "No, maternity leave does NOT count against your PTO balance.")
    23. Cite the specific document section that addresses this relationship
    24. If the relationship isn't explicitly stated in the documents, acknowledge this and provide the most relevant information from both benefits
    25. Explain how the benefits interact in practice for employees
    
    The reader wants to understand the practical differences between these benefits and how they might affect them.
    Focus on providing specific details such as coverage amounts, eligibility requirements, enrollment periods,
    and usage processes.
    
    Example response for a relationship question like "Does maternity leave count against PTO?":
    "No, maternity leave does NOT count against your PTO balance. According to our Parental Leave Policy, maternity leave is a separate benefit that provides X weeks of paid leave following childbirth or adoption. This is completely separate from your PTO balance, which remains intact during your maternity leave. You will continue to accrue PTO while on maternity leave as stated in section X of the policy."
    """
    )
    ```
    
    This code defines a specialized prompt template for comparative questions that provides instructions on how to structure responses that compare different benefits or explain relationships between benefits.
    
    **Step 13.6**. Find the TODO comment: "5. Specialized prompt for follow-up questions" and add this code snippet:
    
    ```python
    self.followup_prompt = ChatPromptTemplate.from_template(
        """
    You are Jenna, an AI HR assistant for Gem City Technologies. Your task is to answer follow-up questions about employee benefits.
    
    Use ONLY the following context to answer the question. If you don't have enough information based on the context, say 
    "I don't have enough information about that in my knowledge base. Please contact HR for more details."
    
    Previous question: {previous_question}
    
    Context from both the current and previous conversation:
    {context}
    
    Current follow-up question: {question}
    
    Important instructions for follow-up questions:
    26. Remember that the user is referring to information from their previous question
    27. Use the combined context to provide a comprehensive answer
    28. Make sure to explain any terms or concepts that carry over from the previous exchange
    29. Include the source document name in your response for citation
    
    Answer the follow-up question based only on the provided context. Format your response in a friendly, helpful tone.
    """
    )
    ```
    
    This code defines a specialized prompt template for follow-up questions that provides instructions on how to handle questions that reference previous conversations.
    
    **Step 13.7**. Find the TODO comment: "6. Initialize the output parser for the response" and add this code snippet:
    
    ```python
    self.parser = StrOutputParser()
    ```
    
    This code initializes a string output parser that will be used to process the responses from the language model.
    
    **Step 13.8**. Find the TODO comment: "1. Read all benefit files from the specified directories" and add this code snippet:
    
    ```python
    for benefit_dir in ["data/benefits", "data/policies"]:
        if os.path.exists(benefit_dir):
            for benefit_file in os.listdir(benefit_dir):
                if not benefit_file.endswith(".txt"):
                    continue
    
                file_path = os.path.join(benefit_dir, benefit_file)
                try:
                    with open(
                        file_path, "r", encoding="utf-8", errors="replace"
                    ) as f:
                        content = f.read()
                        self.benefit_files[benefit_file] = content
    
                        # Create content hashes of different lengths for partial matching
                        content_lower = content.lower()
                        for length in [100, 200, 300, 500]:
                            if len(content_lower) >= length:
                                content_start = content_lower[:length]
                                hash_key = hashlib.md5(
                                    content_start.encode()
                                ).hexdigest()
                                self.benefit_content_hashes[hash_key] = benefit_file
                except Exception as e:
                    print(f"Error reading {benefit_file}: {e}")
    ```
    
    This code reads all benefit files from the specified directories, stores their content in a dictionary, and creates content hashes of different lengths for partial matching.
    
    **Step 13.9**. Find the TODO comment: "1. Check if the content is empty or None" and add this code snippet:
    
    ```python
    if not content:
        return "Unknown"
    ```
    
    This code checks if the content is empty or None and returns "Unknown" if it is.
    
    **Step 13.10**. Find the TODO comment: "2. Handle both string content and document objects/dictionaries" and add this code snippet:
    
    ```python
    if isinstance(content, dict):
        # It's a dictionary - extract page_content
        content = content.get("page_content", "")
    elif hasattr(content, "page_content"):
        # It's a Document object
        content = content.page_content
    ```
    
    This code handles both string content and document objects/dictionaries by extracting the page_content if available.
    
    **Step 13.11**. Find the TODO comment: "3. If we still don't have content as a string, convert it" and add this code snippet:
    
    ```python
    if not isinstance(content, str):
        content = str(content)
    
    content_lower = content.lower()
    ```
    
    This code converts the content to a string if it's not already a string and creates a lowercase version for case-insensitive matching.
    
    **Step 13.12**. Find the TODO comment: "4. Methods to find the document source" and add this code snippet:
    
    ```python
    # Method 1: Check if the content is directly in a benefit file
    for benefit_file, file_content in self.benefit_files.items():
        if content_lower in file_content.lower():
            return benefit_file
    
    # Method 2: Check content hashes for partial matching
    for length in [100, 200, 300]:
        if len(content_lower) >= length:
            content_start = content_lower[:length]
            hash_key = hashlib.md5(content_start.encode()).hexdigest()
            if hash_key in self.benefit_content_hashes:
                return self.benefit_content_hashes[hash_key]
    
    # Method 3: Check for matching first paragraph
    first_paragraph = (
        content_lower.split("\n\n")[0]
        if "\n\n" in content_lower
        else content_lower[:200]
    )
    for benefit_file, file_content in self.benefit_files.items():
        if first_paragraph in file_content.lower():
            return benefit_file
    
    # Method 4: Try to match based on benefit name in content
    for benefit_file in self.benefit_files.keys():
        benefit_name = (
            os.path.splitext(benefit_file)[0]
            .lower()
            .replace("-", " ")
            .replace("_", " ")
        )
        if benefit_name in content_lower[:300]:
            return benefit_file
    
        # Special handling for common benefit types
        if "benefit" in benefit_file.lower() and "benefit" in content_lower[:300]:
            return benefit_file
        if "health" in benefit_file.lower() and "health" in content_lower[:300]:
            return benefit_file
        if (
            "insurance" in benefit_file.lower()
            and "insurance" in content_lower[:300]
        ):
            return benefit_file
    ```
    
    This code implements four different methods to find the document source: direct content matching, content hash matching, first paragraph matching, and benefit name matching.
    
    **Step 13.13**. Find the TODO comment: "5. Fallback to metadata if available" and add this code snippet:
    
    ```python
    metadata_source = getattr(content, "metadata", {}).get("source_file", "")
    if metadata_source:
        return metadata_source
    
    # Final fallback to best guess based on content keywords
    if "health" in content_lower[:500] or "medical" in content_lower[:500]:
        return "Employee-Benefits-and-Perks-1.txt"
    if "dental" in content_lower[:500] or "vision" in content_lower[:500]:
        return "Employee-Benefits-and-Perks-1.txt"
    if "401k" in content_lower[:500] or "retirement" in content_lower[:500]:
        return "Employee-Benefits-and-Perks-1.txt"
    if "wellness" in content_lower[:500] or "mental health" in content_lower[:500]:
        return "Employee-Wellness-Program-Policy.txt"
    
    return "Employee-Benefits-and-Perks-1.txt"  # Better than "Unknown"
    ```
    
    This code provides fallback mechanisms to identify the document source, including checking metadata and making educated guesses based on content keywords.
    
    **Step 13.14**. Find the TODO comment: "1. Check for specific sensitive keywords in the query" and add this code snippet:
    
    ```python
    sensitive_keywords = [
        "mental health",
        "depression",
        "anxiety",
        "wellness",
        "disability",
        "accommodation",
        "medical condition",
        "illness",
        "injury",
        "stress",
        "burnout",
        "therapy",
        "counseling",
        "eap",
        "assistance program",
        "leave of absence",
        "family leave",
        "pregnancy",
        "maternity",
        "paternity",
        "life insurance",
        "death benefit",
    ]
    return any(keyword in query.lower() for keyword in sensitive_keywords)
    ```
    
    This code checks if the query contains any sensitive keywords and returns True if it does, indicating that the query is about a sensitive topic.
    
    **Step 13.15**. Find the TODO comment: "1. Check if this is a relationship question first" and add this code snippet:
    
    ```python
    if self.is_relationship_question(query):
        return True
    ```
    
    This code checks if the query is a relationship question and returns True if it is, as relationship questions are a type of comparative question.
    
    **Step 13.16**. Find the TODO comment: "2. Check for comparative terms in the query" and add this code snippet:
    
    ```python
    comparative_terms = [
        "compare",
        "comparison",
        "contrast",
        "difference",
        "different",
        "versus",
        " vs ",
        " or ",
        "better",
        "worse",
        "preferred",
        "choose between",
        "similarities",
        "similar",
        "same as",
    ]
    
    # Check for comparative terms
    if any(term in query.lower() for term in comparative_terms):
        return True
    ```
    
    This code checks if the query contains any comparative terms and returns True if it does, indicating that the query is asking for a comparison.
    
    **Step 13.17**. Find the TODO comment: "3. Check for specific benefit types in the query" and add this code snippet:
    
    ```python
    benefit_types = [
        "health",
        "dental",
        "vision",
        "medical",
        "insurance",
        "life insurance",
        "disability",
        "retirement",
        "401k",
        "pension",
        "wellness",
        "gym",
        "reimbursement",
        "tuition",
        "education",
        "parental",
        "maternity",
        "paternity",
        "leave",
        "vacation",
        "pto",
    ]
    ```
    
    This code defines a list of benefit types to check for in the query.
    
    **Step 13.18**. Find the TODO comment: "4. Check if multiple benefit types are mentioned in the query" and add this code snippet:
    
    ```python
    found_types = [benefit for benefit in benefit_types if benefit in query.lower()]
    return len(found_types) > 1
    ```
    
    This code checks if multiple benefit types are mentioned in the query and returns True if they are, indicating that the query is likely asking for a comparison.
    
    **Step 13.19**. Find the TODO comment: "1. Check for specific patterns in the query" and add this code snippet:
    
    ```python
    # Pattern 1: "Does X count against Y"
    count_patterns = [
        "count against",
        "counts against",
        "counted against",
        "counting against",
        "use my",
        "uses my",
        "using my",
        "part of",
        "included in",
        "separate from",
        "affect my",
        "affects my",
        "impact my",
        "impacts my",
    ]
    
    if any(pattern in query_lower for pattern in count_patterns):
        return True
    
    # Pattern 2: "Is X separate from Y"
    if "separate" in query_lower and any(
        benefit in query_lower
        for benefit in [
            "pto",
            "vacation",
            "leave",
            "time off",
            "maternity",
            "paternity",
            "parental",
        ]
    ):
        return True
    
    # Pattern 3: Direct questions about relationships
    relationship_patterns = [
        "how does .* relate to",
        "how do .* relate to",
        "connection between .* and",
        "relationship between .* and",
        "how .* works with",
    ]
    
    for pattern in relationship_patterns:
        if re.search(pattern, query_lower):
            return True
    
    return False
    ```
    
    This code checks for specific patterns in the query that indicate it's asking about relationships between benefits, such as "Does X count against Y" or "Is X separate from Y".
    
    **Step 13.20**. Find the TODO comment: "1. Check for pronouns and demonstratives that reference previous content" and add this code snippet:
    
    ```python
    followup_indicators = [
        "it",
        "this",
        "that",
        "they",
        "them",
        "those",
        "their",
        "its",
        "these",
        "the benefit",
        "the plan",
        "the coverage",
        "the policy",
        "the document",
        "tell me more",
        "explain",
        "elaborate",
        "clarify",
        "what about",
        "how about",
        "how does",
        "how do",
    ]
    ```
    
    This code defines a list of follow-up indicators, such as pronouns and demonstratives, that suggest the query is referencing previous content.
    
    **Step 13.21**. Find the TODO comment: "2. Check if the query contains any follow-up indicators and if it is a short query" and add this code snippet:
    
    ```python
    # Check if the query contains any follow-up indicators
    if any(indicator in query.lower() for indicator in followup_indicators):
        return True
    
    # Check if the query is very short (likely a follow-up)
    if len(query.split()) <= 5:
        return True
    
    return False
    ```
    
    This code checks if the query contains any follow-up indicators or if it's very short, both of which suggest it's a follow-up question.
    
    **Step 13.22**. Find the TODO comment: "1. map of terms to their related terms for expansion" and add this code snippet:
    
    ```python
    expanded_query = query
    
    # Map of terms to their related terms for expansion
    term_expansions = {
        "health": "medical healthcare insurance wellness doctor",
        "dental": "dentist teeth orthodontic dental insurance",
        "vision": "eye glasses contacts vision insurance optometrist",
        "retirement": "401k pension retirement plan savings future",
        "parental": "maternal paternity maternity leave baby child",
        "disability": "short-term long-term disability insurance ada",
        "leave": "time off absence pto vacation holiday",
        "vacation": "time off pto leave holiday break",
        "wellness": "fitness health gym mental physical wellbeing",
        "mental health": "counseling therapy eap stress burnout assistance",
        "life insurance": "death benefit survivor dependent coverage term",
    }
    ```
    
    This code initializes the expanded query and defines a map of terms to their related terms for expansion.
    
    **Step 13.23**. Find the TODO comment: "2. Add related terms to the query and return the expanded query" and add this code snippet:
    
    ```python
    for term, expansion in term_expansions.items():
        if term in query.lower() and not all(
            exp in query.lower() for exp in expansion.split()
        ):
            expanded_query += f" {expansion}"
    
    return expanded_query
    ```
    
    This code adds related terms to the query if they're not already present and returns the expanded query.
    
    **Step 13.24**. Find the TODO comment: "1. Check for common benefit entities" and add this code snippet:
    
    ```python
    benefit_entities = {
        "health": ["health", "healthcare", "medical", "insurance"],
        "dental": ["dental", "teeth", "dentist"],
        "vision": ["vision", "eye", "glasses", "contacts"],
        "retirement": ["retirement", "401k", "pension", "savings"],
        "parental": ["parental", "maternity", "paternity", "baby", "child"],
        "disability": ["disability", "ada", "accommodation"],
        "leave": ["leave", "time off", "pto", "vacation"],
        "wellness": ["wellness", "fitness", "gym", "wellbeing"],
        "mental health": ["mental health", "counseling", "therapy", "eap"],
        "life insurance": ["life insurance", "death benefit", "survivor"],
    }
    ```
    
    This code defines a dictionary of benefit entities and their associated keywords.
    
    **Step 13.25**. Find the TODO comment: "2. Check for each entity type in the query and return the found entities" and add this code snippet:
    
    ```python
    found_entities = []
    
    # Look for each entity type in the query
    for entity_type, keywords in benefit_entities.items():
        if any(keyword in query.lower() for keyword in keywords):
            found_entities.append(entity_type)
    
    return found_entities
    ```
    
    This code checks for each entity type in the query and returns a list of found entities.
    
    **Step 13.26**. Find the TODO comment: "1. Check if the vector store is available" and add this code snippet:
    
    ```python
    if not self.vector_store:
        return []
    ```
    
    This code checks if the vector store is available and returns an empty list if it's not.
    
    **Step 13.27**. Find the TODO comment: "2. Check if this is a comparative question and expand the query" and add this code snippet:
    
    ```python
    is_comparative = self.is_comparative_question(query)
    
    # Create expanded query for better retrieval
    expanded_query = self.expand_query(query)
    ```
    
    This code checks if the query is a comparative question and expands the query with related terms for better retrieval.
    
    **Step 13.28**. Find the TODO comment: "3. Get retriever without filter to ensure we get documents and print debug info" and add this code snippet:
    
    ```python
    retriever = self.vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k if not is_comparative else k * 2
        },  # Get more docs for comparative questions
    )
    
    # Print original and expanded query for debugging
    if expanded_query != query:
        print(f"\nOriginal query: '{query}'")
        print(f"Expanded query: '{expanded_query}'")
    ```
    
    This code gets a retriever without a filter to ensure we get documents and prints debug information about the original and expanded queries.
    
    **Step 13.29**. Find the TODO comment: "4. Try to get documents using the expanded query" and add this code snippet:
    
    ```python
    docs = retriever.invoke(expanded_query)
    ```
    
    This code retrieves documents using the expanded query.
    
    **Step 13.30**. Find the TODO comment: "5. For comparative questions, we need a second phase of retrieval" and add this code snippet:
    
    ```python
    if is_comparative:
        entities = self.extract_entities_for_comparison(query)
        if len(entities) > 1:
            print(f"Detected comparative question about: {', '.join(entities)}")
    
            # Create individual queries for each entity
            entity_docs = []
            for entity in entities:
                entity_query = f"{entity} benefit"
                entity_docs.extend(retriever.invoke(entity_query))
    
            # Add these entity-specific docs to our results
            docs.extend(entity_docs)
    
            # Remove duplicates while preserving order
            seen = set()
            unique_docs = []
            for doc in docs:
                doc_id = doc.page_content[
                    :100
                ]  # Use first 100 chars as a simple ID
                if doc_id not in seen:
                    seen.add(doc_id)
                    unique_docs.append(doc)
    
            docs = unique_docs[
                : k + 5
            ]  # Limit to slightly more than k to have enough context
    ```
    
    This code performs a second phase of retrieval for comparative questions by creating individual queries for each entity and adding the results to the original documents.
    
    **Step 13.31**. Find the TODO comment: "6. Additional handling for sensitive topics" and add this code snippet:
    
    ```python
    if self.is_sensitive_topic(query):
        # Try to find relevant sensitive topic documents
        sensitive_topic_keywords = [
            keyword
            for keyword in [
                "mental health",
                "wellness",
                "disability",
                "accommodation",
                "leave",
                "counseling",
                "assistance program",
                "life insurance",
            ]
            if keyword in query.lower()
        ]
    
        if sensitive_topic_keywords:
            for keyword in sensitive_topic_keywords:
                topic_docs = retriever.invoke(keyword)
                docs.extend(topic_docs)
    
            # Remove duplicates
            seen = set()
            unique_docs = []
            for doc in docs:
                doc_id = doc.page_content[:100]
                if doc_id not in seen:
                    seen.add(doc_id)
                    unique_docs.append(doc)
    
            docs = unique_docs[: k + 5]
    ```
    
    This code provides additional handling for sensitive topics by retrieving documents specifically related to the sensitive keywords in the query.
    
    **Step 13.32**. Find the TODO comment: "7. Print document information for debugging with improved filename detection" and add this code snippet:
    
    ```python
    print(f"\nRetrieved {len(docs)} documents for query: '{query}'")
    for i, doc in enumerate(docs):
        # Use the improved document source finder
        file_match = self.find_document_source(doc.page_content)
    
        source_type = doc.metadata.get("source", "Unknown")
        print(f"  Doc {i+1}: {file_match} (Type: {source_type})")
    
        # Replace "First 100 chars:" with "Preview:"
        preview = doc.page_content[:100].replace(chr(10), " ")
        if len(doc.page_content) > 100:
            preview += "..."
        print(f"  Preview: {preview}")
    ```
    
    This code prints document information for debugging, including the document source and a preview of the content.
    
    **Step 13.33**. Find the TODO comment: "8. Implement special handling for various query types" and add this code snippet:
    
    ```python
    # Health benefit queries
    if any(term in query.lower() for term in ["health", "medical", "insurance"]):
        print("  Health benefit query detected, returning all documents")
        print("\n")
        return docs
    
    # Mental health queries
    if (
        "mental health" in query.lower()
        or "wellness" in query.lower()
        or "eap" in query.lower()
    ):
        print("  Mental health/wellness query detected, returning all documents")
        print("\n")
        return docs
    
    # Retirement benefit queries
    if (
        "retirement" in query.lower()
        or "401k" in query.lower()
        or "pension" in query.lower()
    ):
        print("  Retirement benefit query detected, returning all documents")
        print("\n")
        return docs
    
    # Comparative queries need documents from multiple categories
    if is_comparative:
        print("  Comparative query detected, returning all documents")
        print("\n")
        return docs
    ```
    
    This code implements special handling for various query types, such as health benefit queries, mental health queries, retirement benefit queries, and comparative queries.
    
    **Step 13.34**. Find the TODO comment: "9. Filter to benefit documents manually if needed, add extra blank lines, and return" and add this code snippet:
    
    ```python
    benefit_docs = [doc for doc in docs if doc.metadata.get("source") == "benefit"]
    
    # Add extra blank lines for readability before Jenna's response
    print("\n")
    
    # If no benefit docs found, return all docs instead of an empty list
    return benefit_docs if benefit_docs else docs
    ```
    
    This code filters to benefit documents manually if needed, adds extra blank lines for readability, and returns the filtered documents or all documents if no benefit documents are found.
    
    **Step 13.35**. Find the TODO comment: "1. Check if the documents are empty" and add this code snippet:
    
    ```python
    if not documents:
        return "I don't have enough information about that in my knowledge base. Please contact HR for more details."
    ```
    
    This code checks if the documents are empty and returns a default message if they are.
    
    **Step 13.36**. Find the TODO comment: "2. Format context from documents with improved source information and grouping" and add this code snippet:
    
    ```python
    formatted_docs = []
    doc_by_benefit = {}  # Group documents by benefit type
    
    for doc in documents:
        # Use the improved document source finder
        file_match = self.find_document_source(doc.page_content)
    
        # For comparative questions, group by benefit type
        if self.is_comparative_question(query):
            benefit_type = (
                file_match.split("-")[0] if "-" in file_match else file_match
            )
            if benefit_type not in doc_by_benefit:
                doc_by_benefit[benefit_type] = []
            doc_by_benefit[benefit_type].append(
                f"Document: {file_match}\n{doc.page_content}"
            )
        else:
            formatted_docs.append(f"Document: {file_match}\n{doc.page_content}")
    ```
    
    This code formats context from documents with improved source information and grouping, organizing documents by benefit type for comparative questions.
    
    **Step 13.37**. Find the TODO comment: "3. If this is a comparative question, organize context by benefit type" and add this code snippet:
    
    ```python
    if self.is_comparative_question(query) and doc_by_benefit:
        for benefit_type, docs in doc_by_benefit.items():
            formatted_docs.append(f"--- {benefit_type} BENEFIT INFORMATION ---")
            formatted_docs.extend(docs)
    
    context = "\n\n".join(formatted_docs)
    ```
    
    This code organizes context by benefit type for comparative questions and joins all formatted documents into a single context string.
    
    **Step 13.38**. Find the TODO comment: "4. Select the appropriate prompt based on query type" and add this code snippet:
    
    ```python
    if self.is_followup_question(query, previous_question) and previous_question:
        print("  Using specialized follow-up question prompt")
        # For follow-up questions, include the previous question in the prompt
        chain = self.followup_prompt | self.llm | self.parser
        response = chain.invoke(
            {
                "context": context,
                "question": query,
                "previous_question": previous_question,
            }
        )
    elif self.is_comparative_question(query):
        print("  Using specialized comparative question prompt")
        chain = self.comparison_prompt | self.llm | self.parser
        response = chain.invoke({"context": context, "question": query})
    elif self.is_sensitive_topic(query):
        print("  Using specialized sensitive topic prompt")
        chain = self.sensitive_topic_prompt | self.llm | self.parser
        response = chain.invoke({"context": context, "question": query})
    else:
        print("  Using standard QA prompt")
        chain = self.qa_prompt | self.llm | self.parser
        response = chain.invoke({"context": context, "question": query})
    
    return response
    ```
    
    This code selects the appropriate prompt based on the query type (follow-up, comparative, sensitive, or standard) and generates a response using the selected prompt.



## Task 14: Implement `PolicyRAG` Class

The `policy_qa.py` file contains the `PolicyRAG` class, which handles policy-related queries using retrieval-augmented generation. 

Similar to BenefitsRAG, this class requires implementing these key methods:

The constructor initializes the vector store, builds a policy file cache, and sets up specialized prompt templates. `_build_policy_cache` reads policy files and creates content hashes for partial matching. `find_document_source` identifies source documents using multiple techniques.

`is_sensitive_topic` detects queries about sensitive workplace topics like substance abuse or harassment. `is_comparative_question` and `is_relationship_question` identify queries comparing policies or asking about policy relationships. `is_followup_question` detects follow-up queries.

`expand_query` enhances queries with related terms to improve retrieval. `extract_entities_for_comparison` identifies policy entities in comparative queries. `get_relevant_documents` retrieves documents with special handling for comparative and sensitive topics. `generate_response` creates responses using appropriate prompt templates based on query type.

This class ensures accurate, contextually appropriate responses to questions about company policies and procedures.

14. **Implement `PolicyRAG` Class**

    **Step 14.1**. Find the TODO comment: "Implement the PolicyRAG class to handle policy-related queries" and follow the steps below.
    
    **Step 14.2**. Find the TODO comment: "1. Define the constructor to initialize the class with LLM and vector store" and add this code snippet:
    
    ```python
    def __init__(self, llm, vector_store_path="data/vector_store"):
        """Initialize the Policy RAG component"""
        self.llm = llm
        try:
            self.vector_store = load_vector_store(vector_store_path)
        except FileNotFoundError:
            # If vector store doesn't exist yet, we'll initialize with empty retriever
            # It will be populated later during setup
            self.vector_store = None
    
        # Build a content cache of policy files for better matching
        self.policy_files = {}
        self.policy_content_hashes = {}
        self._build_policy_cache()
    ```
    
    This code initializes the PolicyRAG class with an LLM model and vector store path. It tries to load the vector store or initializes it as None if not found. It also sets up empty dictionaries for policy files and content hashes, then calls the `_build_policy_cache` method.
    
    **Step 14.3**. Find the TODO comment: "1. Ensure the directories exist and load policy files" and add this code snippet:
    
    ```python
    for policy_dir in ["data/policies", "data/benefits"]:
        if os.path.exists(policy_dir):
            for policy_file in os.listdir(policy_dir):
                if not policy_file.endswith(".txt"):
                    continue
    
                file_path = os.path.join(policy_dir, policy_file)
                try:
                    with open(
                        file_path, "r", encoding="utf-8", errors="replace"
                    ) as f:
                        content = f.read()
                        self.policy_files[policy_file] = content
    
                        # Create content hashes of different lengths for partial matching
                        content_lower = content.lower()
                        for length in [100, 200, 300, 500]:
                            if len(content_lower) >= length:
                                content_start = content_lower[:length]
                                hash_key = hashlib.md5(
                                    content_start.encode()
                                ).hexdigest()
                                self.policy_content_hashes[hash_key] = policy_file
                except Exception as e:
                    print(f"Error reading {policy_file}: {e}")
    ```
    
    This code reads all .txt files from the policies and benefits directories, stores their content in the policy_files dictionary, and creates content hashes of different lengths for partial matching.
    
    **Step 14.4**. Find the TODO comment: "1. Check if the content is empty or None and handle string conversion" and add this code snippet:
    
    ```python
    if not content:
        return "Unknown"
    
    # Handle both string content and document objects/dictionaries
    if isinstance(content, dict):
        # It's a dictionary - extract page_content
        content = content.get("page_content", "")
    elif hasattr(content, "page_content"):
        # It's a Document object
        content = content.page_content
    
    # If we still don't have content as a string, convert it
    if not isinstance(content, str):
        content = str(content)
    
    content_lower = content.lower()
    ```
    
    This code checks if the content is empty and handles different types of content (dictionary, Document object, or string) to extract the text content.
    
    **Step 14.5**. Find the TODO comment: "2. Methods to find the source document" and add this code snippet:
    
    ```python
    # Method 1: Check if the content is directly in a policy file
    for policy_file, file_content in self.policy_files.items():
        if content_lower in file_content.lower():
            return policy_file
    
    # Method 2: Check content hashes for partial matching
    for length in [100, 200, 300]:
        if len(content_lower) >= length:
            content_start = content_lower[:length]
            hash_key = hashlib.md5(content_start.encode()).hexdigest()
            if hash_key in self.policy_content_hashes:
                return self.policy_content_hashes[hash_key]
    
    # Method 3: Check for matching first paragraph
    first_paragraph = (
        content_lower.split("\n\n")[0]
        if "\n\n" in content_lower
        else content_lower[:200]
    )
    for policy_file, file_content in self.policy_files.items():
        if first_paragraph in file_content.lower():
            return policy_file
    
    # Method 4: Try to match based on policy name in content
    for policy_file in self.policy_files.keys():
        policy_name = (
            os.path.splitext(policy_file)[0]
            .lower()
            .replace("-", " ")
            .replace("_", " ")
        )
        if policy_name in content_lower[:300]:
            return policy_file
    
        # Special handling for common policy types
        if "pto" in policy_file.lower() and "pto" in content_lower[:300]:
            return policy_file
        if "vacation" in policy_file.lower() and "vacation" in content_lower[:300]:
            return policy_file
        if (
            "credit card" in policy_file.lower()
            and "credit card" in content_lower[:300]
        ):
            return policy_file
    ```
    
    This code uses multiple methods to find the source document for a given content, including direct content matching, hash-based matching, first paragraph matching, and policy name matching.
    
    **Step 14.6**. Find the TODO comment: "5. Fallback to metadata if available" and add this code snippet:
    
    ```python
    metadata_source = getattr(content, "metadata", {}).get("source_file", "")
    if metadata_source:
        return metadata_source
    
    # Final fallback to best guess based on content keywords
    if "credit card" in content_lower[:500]:
        return "Company-credit-card-policy.txt"
    if "pto" in content_lower[:500] or "paid time off" in content_lower[:500]:
        return "Employee_PTO_policy_sample.txt"
    if "sick leave" in content_lower[:500]:
        return "Sample-company-sick-leave-policy.txt"
    if "substance abuse" in content_lower[:500] or "drug" in content_lower[:500]:
        return "Substance-abuse-company-policy.txt"
    if "mental health" in content_lower[:500]:
        return "Employer-mental-health-policy-template.txt"
    
    return "Company-policies-general.txt"  # Better than "Unknown"
    ```
    
    This code provides fallback methods to identify the source document, including checking metadata and using keyword-based matching for common policy types.
    
    **Step 14.7**. Find the TODO comment: "1. Check if the query contains any sensitive keywords" and add this code snippet:
    
    ```python
    sensitive_keywords = [
        "substance abuse",
        "drug",
        "alcohol",
        "addiction",
        "mental health",
        "depression",
        "anxiety",
        "harassment",
        "discrimination",
        "sexual harassment",
        "bullying",
        "violence",
        "terminate",
        "termination",
        "firing",
        "layoff",
        "disability",
        "medical condition",
        "illness",
        "injury",
    ]
    return any(keyword in query.lower() for keyword in sensitive_keywords)
    ```
    
    This code checks if the query contains any sensitive keywords related to substance abuse, mental health, harassment, termination, or medical conditions.
    
    **Step 14.8**. Find the TODO comment: "1. Check if this is a relationship question first" and add this code snippet:
    
    ```python
    if self.is_relationship_question(query):
        return True
    ```
    
    This code first checks if the query is a relationship question, which is a type of comparative question.
    
    **Step 14.9**. Find the TODO comment: "2. Check for comparative terms in the query" and add this code snippet:
    
    ```python
    comparative_terms = [
        "compare",
        "comparison",
        "contrast",
        "difference",
        "different",
        "versus",
        " vs ",
        " or ",
        "better",
        "worse",
        "preferred",
        "choose between",
        "similarities",
        "similar",
        "same as",
    ]
    
    # Check for comparative terms
    if any(term in query.lower() for term in comparative_terms):
        return True
    ```
    
    This code checks if the query contains any comparative terms that indicate the user is asking for a comparison between policies.
    
    **Step 14.10**. Find the TODO comment: "3. Check for multiple policy types in the query" and add this code snippet:
    
    ```python
    policy_types = [
        "pto",
        "vacation",
        "time off",
        "leave",
        "sick",
        "maternity",
        "paternity",
        "parental",
        "bereavement",
        "holiday",
        "benefits",
        "insurance",
        "health",
        "dental",
        "vision",
        "retirement",
        "401k",
        "compensation",
        "bonus",
    ]
    
    found_types = [policy for policy in policy_types if policy in query.lower()]
    return len(found_types) > 1
    ```
    
    This code checks if the query mentions multiple policy types, which would indicate a comparative question.
    
    **Step 14.11**. Find the TODO comment: "1. Check if the query contains any patterns indicating a relationship" and add this code snippet:
    
    ```python
    query_lower = query.lower()
    
    # Pattern 1: "Does X count against Y"
    count_patterns = [
        "count against",
        "counts against",
        "counted against",
        "counting against",
        "use my",
        "uses my",
        "using my",
        "part of",
        "included in",
        "separate from",
        "affect my",
        "affects my",
        "impact my",
        "impacts my",
    ]
    
    if any(pattern in query_lower for pattern in count_patterns):
        return True
    
    # Pattern 2: "Is X separate from Y"
    if "separate" in query_lower and any(
        policy in query_lower for policy in ["pto", "vacation", "leave", "time off"]
    ):
        return True
    
    # Pattern 3: Direct questions about relationships
    relationship_patterns = [
        "how does .* relate to",
        "how do .* relate to",
        "connection between .* and",
        "relationship between .* and",
        "how .* works with",
    ]
    
    for pattern in relationship_patterns:
        if re.search(pattern, query_lower):
            return True
    
    return False
    ```
    
    This code checks for various patterns that indicate the query is asking about relationships between policies, such as "Does X count against Y" or "Is X separate from Y".
    
    **Step 14.12**. Find the TODO comment: "1. Check if the query is empty or None" and add this code snippet:
    
    ```python
    if not previous_question:
        return False
    ```
    
    This code checks if there is a previous question to compare against. If not, it cannot be a follow-up question.
    
    **Step 14.13**. Find the TODO comment: "2. Check if the query is a follow-up to the previous question" and add this code snippet:
    
    ```python
    # Check for pronouns and demonstratives that reference previous content
    followup_indicators = [
        "it",
        "this",
        "that",
        "they",
        "them",
        "those",
        "their",
        "its",
        "these",
        "the policy",
        "the document",
        "the rule",
        "the benefit",
        "tell me more",
        "explain",
        "elaborate",
        "clarify",
        "what about",
        "how about",
    ]
    ```
    
    This code defines a list of follow-up indicators, which are words or phrases that typically indicate a follow-up question.
    
    **Step 14.14**. Find the TODO comment: "3. Check if the query contains any follow-up indicators and if it is short" and add this code snippet:
    
    ```python
    if any(indicator in query.lower() for indicator in followup_indicators):
        return True
    
    # Check if the query is very short (likely a follow-up)
    if len(query.split()) <= 5:
        return True
    
    return False
    ```
    
    This code checks if the query contains any follow-up indicators or if it is very short (5 words or less), which would likely indicate a follow-up question.
    
    **Step 14.15**. Find the TODO comment: "1. Map of terms to their related terms for expansion" and add this code snippet:
    
    ```python
    expanded_query = query
    
    # Map of terms to their related terms for expansion
    term_expansions = {
        "pto": "paid time off vacation leave holiday",
        "vacation": "pto paid time off leave holiday",
        "sick": "sick leave illness medical health",
        "maternity": "maternity leave parental pregnancy childbirth",
        "paternity": "paternity leave parental childcare",
        "health": "medical insurance healthcare benefits wellness",
        "retirement": "401k pension retirement benefits",
        "bonus": "compensation bonus incentive payment reward",
        "credit card": "company card corporate card expense card",
        "substance abuse": "drug alcohol addiction treatment support recovery wellness eap assistance program",
        "addiction": "substance abuse drug alcohol treatment support recovery wellness eap assistance program",
        "mental health": "wellness counseling therapy psychological support eap assistance program",
        "eap": "employee assistance program counseling mental health support wellness",
        "assistance program": "eap employee assistance counseling mental health support",
        "wellness program": "health wellness mental physical wellbeing benefits",
        "discrimination": "equality diversity inclusion harassment rights",
        "harassment": "bullying inappropriate behavior hostile work environment",
    }
    ```
    
    This code creates a mapping of terms to their related terms for query expansion, which will help improve document retrieval.
    
    **Step 14.16**. Find the TODO comment: "2. Add related terms to the query" and add this code snippet:
    
    ```python
    for term, expansion in term_expansions.items():
        if term in query.lower() and not all(
            exp in query.lower() for exp in expansion.split()
        ):
            expanded_query += f" {expansion}"
    ```
    
    This code adds related terms to the query for each term found in the query, but only if those related terms aren't already present.
    
    **Step 14.17**. Find the TODO comment: "3. Special handling for addiction/substance abuse questions about options or help" and add this code snippet:
    
    ```python
    help_terms = ["help", "option", "support", "resource", "assist", "program"]
    addiction_terms = ["addict", "substance", "drug", "alcohol"]
    
    if any(help in query.lower() for help in help_terms) and any(
        addiction in query.lower() for addiction in addiction_terms
    ):
        expanded_query += " employee assistance program eap wellness support recovery treatment counseling"
    
    return expanded_query
    ```
    
    This code adds specific terms related to employee assistance programs when the query is about addiction/substance abuse and help options.
    
    **Step 14.18**. Find the TODO comment: "1. Check for common policy entities in the query" and add this code snippet:
    
    ```python
    policy_entities = {
        "pto": ["pto", "paid time off", "vacation", "time off", "leave"],
        "sick": ["sick", "sick leave", "illness", "medical leave"],
        "maternity": ["maternity", "maternity leave", "pregnancy leave"],
        "paternity": ["paternity", "paternity leave", "parental leave"],
        "health": ["health", "health insurance", "medical", "healthcare"],
        "retirement": ["401k", "retirement", "pension"],
        "compensation": ["salary", "compensation", "pay", "bonus", "incentive"],
        "credit card": [
            "credit card",
            "company card",
            "corporate card",
            "expense card",
        ],
        "substance abuse": ["substance abuse", "drug", "alcohol", "addiction"],
        "mental health": [
            "mental health",
            "wellness",
            "psychological",
            "counseling",
        ],
    }
    
    found_entities = []
    
    # Look for each entity type in the query
    for entity_type, keywords in policy_entities.items():
        if any(keyword in query.lower() for keyword in keywords):
            found_entities.append(entity_type)
    
    return found_entities
    ```
    
    This code identifies policy entities mentioned in the query by checking for keywords associated with each entity type.
    
    **Step 14.19**. Find the TODO comment: "1. Check if the vector store is available" and add this code snippet:
    
    ```python
    if not self.vector_store:
        return []
    ```
    
    This code checks if the vector store is available. If not, it returns an empty list.
    
    **Step 14.20**. Find the TODO comment: "2. Check if this is a comparative question and create an expanded query" and add this code snippet:
    
    ```python
    is_comparative = self.is_comparative_question(query)
    
    # Create expanded query for better retrieval
    expanded_query = self.expand_query(query)
    ```
    
    This code checks if the query is a comparative question and creates an expanded query with related terms for better retrieval.
    
    **Step 14.21**. Find the TODO comment: "3. Get retriever without filter to ensure we get documents, print original query, and get documents" and add this code snippet:
    
    ```python
    retriever = self.vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k if not is_comparative else k * 2
        },  # Get more docs for comparative questions
    )
    
    # Print original and expanded query for debugging
    if expanded_query != query:
        print(f"\nOriginal query: '{query}'")
        print(f"Expanded query: '{expanded_query}'")
    
    # Try to get documents using the expanded query
    docs = retriever.invoke(expanded_query)
    ```
    
    This code creates a retriever with the appropriate search parameters, prints the original and expanded queries for debugging, and retrieves documents using the expanded query.
    
    **Step 14.22**. Find the TODO comment: "4. For comparative questions, we need a second phase of retrieval" and add this code snippet:
    
    ```python
    if is_comparative:
        entities = self.extract_entities_for_comparison(query)
        if len(entities) > 1:
            print(f"Detected comparative question about: {', '.join(entities)}")
    
            # Create individual queries for each entity
            entity_docs = []
            for entity in entities:
                entity_query = f"{entity} policy"
                entity_docs.extend(retriever.invoke(entity_query))
    
            # Add these entity-specific docs to our results
            docs.extend(entity_docs)
    
            # Remove duplicates while preserving order
            seen = set()
            unique_docs = []
            for doc in docs:
                doc_id = doc.page_content[
                    :100
                ]  # Use first 100 chars as a simple ID
                if doc_id not in seen:
                    seen.add(doc_id)
                    unique_docs.append(doc)
    
            docs = unique_docs[
                : k + 5
            ]  # Limit to slightly more than k to have enough context
    ```
    
    This code performs a second phase of retrieval for comparative questions by creating individual queries for each entity mentioned in the query, retrieving documents for each entity, and combining the results while removing duplicates.
    
    **Step 14.23**. Find the TODO comment: "5. Additional handling for sensitive topics" and add this code snippet:
    
    ```python
    if self.is_sensitive_topic(query):
        # Try to find relevant sensitive topic documents
        sensitive_topic_keywords = [
            keyword
            for keyword in [
                "substance abuse",
                "drug",
                "alcohol",
                "mental health",
                "harassment",
                "discrimination",
                "disability",
                "termination",
            ]
            if keyword in query.lower()
        ]
        if sensitive_topic_keywords:
            for keyword in sensitive_topic_keywords:
                topic_docs = retriever.invoke(keyword)
                docs.extend(topic_docs)
    
            # Remove duplicates
            seen = set()
            unique_docs = []
            for doc in docs:
                doc_id = doc.page_content[:100]
                if doc_id not in seen:
                    seen.add(doc_id)
                    unique_docs.append(doc)
    
            docs = unique_docs[: k + 5]
    ```
    
    This code provides additional handling for sensitive topics by retrieving documents specifically related to the sensitive keywords found in the query.
    
    **Step 14.24**. Find the TODO comment: "6. Print document information for debugging with improved filename detection" and add this code snippet:
    
    ```python
    print(f"\nRetrieved {len(docs)} documents for query: '{query}'")
    for i, doc in enumerate(docs):
        # Use the improved document source finder
        file_match = self.find_document_source(doc.page_content)
    
        source_type = doc.metadata.get("source", "Unknown")
        print(f"  Doc {i+1}: {file_match} (Type: {source_type})")
    
        # Replace "First 100 chars:" with "Preview:"
        preview = doc.page_content[:100].replace(chr(10), " ")
        if len(doc.page_content) > 100:
            preview += "..."
        print(f"  Preview: {preview}")
    ```
    
    This code prints information about the retrieved documents, including the source file, source type, and a preview of the content.
    
    **Step 14.25**. Find the TODO comment: "7. Special handling for various query types" and add this code snippet:
    
    ```python
    # PTO queries
    if (
        "pto" in query.lower()
        or "time off" in query.lower()
        or "vacation" in query.lower()
    ):
        print("  PTO query detected, returning all documents")
        print("\n")  # Add extra blank lines for readability before Jenna's response
        return docs
    
    # Credit card queries
    if "credit card" in query.lower() or "company card" in query.lower():
        print("  Credit card query detected, returning all documents")
        print("\n")
        return docs
    
    # Substance abuse queries
    if (
        "substance abuse" in query.lower()
        or "drug" in query.lower()
        or "alcohol" in query.lower()
    ):
        print("  Substance abuse query detected, returning all documents")
        print("\n")
        return docs
    
    # Mental health queries
    if "mental health" in query.lower() or "wellness" in query.lower():
        print("  Mental health query detected, returning all documents")
        print("\n")
        return docs
    
    # Comparative queries need documents from multiple categories
    if is_comparative:
        print("  Comparative query detected, returning all documents")
        print("\n")
        return docs
    
    # Filter to policy documents manually if needed
    policy_docs = [doc for doc in docs if doc.metadata.get("source") == "policy"]
    
    # If no policy docs found, return all docs instead of an empty list
    return policy_docs if policy_docs else docs
    ```
    
    This code provides special handling for various query types, including PTO, credit card, substance abuse, mental health, and comparative queries. It returns all documents for these specific query types and filters to policy documents for other queries.
    
    **Step 14.26**. Find the TODO comment: "1. Check if the documents are empty and format the response accordingly" and add this code snippet:
    
    ```python
    if not documents:
        return "I don't have enough information about that in my knowledge base. Please contact HR for more details."
    
    # Format context from documents with improved source information and grouping
    formatted_docs = []
    doc_by_policy = {}  # Group documents by policy type
    ```
    
    This code checks if there are any documents available. If not, it returns a default message. Otherwise, it initializes variables for formatting the context.
    
    **Step 14.27**. Find the TODO comment: "2. Iterate through the documents and extract page_content and metadata" and add this code snippet:
    
    ```python
    for doc in documents:
        # Extract page_content safely from either Document objects or dictionaries
        if isinstance(doc, dict):
            page_content = doc.get("page_content", "")
            metadata = doc.get("metadata", {})
        else:
            # Assume it's a Document object or similar
            page_content = getattr(doc, "page_content", str(doc))
            metadata = getattr(doc, "metadata", {})
    
        # Use the improved document source finder
        file_match = self.find_document_source(doc)
    
        # For comparative questions, group by policy type
        if self.is_comparative_question(query):
            policy_type = (
                file_match.split("-")[0] if "-" in file_match else file_match
            )
            if policy_type not in doc_by_policy:
                doc_by_policy[policy_type] = []
            doc_by_policy[policy_type].append(
                f"Document: {file_match}\n{page_content}"
            )
        else:
            formatted_docs.append(f"Document: {file_match}\n{page_content}")
    ```
    
    This code iterates through the documents, extracts the page content and metadata, and formats the documents based on whether the query is a comparative question or not.
    
    **Step 14.28**. Find the TODO comment: "3. Organize context by policy type for comparative questions" and add this code snippet:
    
    ```python
    if self.is_comparative_question(query) and doc_by_policy:
        for policy_type, docs in doc_by_policy.items():
            formatted_docs.append(f"--- {policy_type} POLICY INFORMATION ---")
            formatted_docs.extend(docs)
    
    context = "\n\n".join(formatted_docs)
    ```
    
    This code organizes the context by policy type for comparative questions and joins all formatted documents with double newlines.
    
    **Step 14.29**. Find the TODO comment: "4. Select the appropriate prompt based on query type" and add this code snippet:
    
    ```python
    if self.is_followup_question(query, previous_question) and previous_question:
        print("  Using specialized follow-up question prompt")
        # For follow-up questions, include the previous question in the prompt
        chain = self.followup_prompt | self.llm | self.parser
        response = chain.invoke(
            {
                "context": context,
                "question": query,
                "previous_question": previous_question,
            }
        )
    elif self.is_comparative_question(query):
        print("  Using specialized comparative question prompt")
        chain = self.comparison_prompt | self.llm | self.parser
        response = chain.invoke({"context": context, "question": query})
    elif self.is_sensitive_topic(query):
        print("  Using specialized sensitive topic prompt")
        chain = self.sensitive_topic_prompt | self.llm | self.parser
        response = chain.invoke({"context": context, "question": query})
    else:
        print("  Using standard QA prompt")
        chain = self.qa_prompt | self.llm | self.parser
        response = chain.invoke({"context": context, "question": query})
    
    return response
    ```
    
    This code selects the appropriate prompt based on the query type (follow-up, comparative, sensitive, or standard) and generates a response using the selected prompt and the LLM.


## Testing




## Extension Challenges

### 1. Multi-Turn Conversation Enhancement

**Challenge**: Implement a more sophisticated conversation memory system that can handle complex multi-turn conversations.

**Implementation Ideas**:
- Create a conversation summarization feature that maintains the gist of longer conversations
- Implement a relevance scoring algorithm to prioritize more important context
- Add support for explicit reference resolution (e.g., "Tell me more about the second point you mentioned")
- Develop a mechanism to detect and recover from conversation context loss

### 2. Advanced RAG System Optimizations

**Challenge**: Enhance the RAG system with more advanced retrieval techniques.

**Implementation Ideas**:
- Implement hybrid search that combines keyword and semantic search
- Add a reranking mechanism to improve retrieval precision
- Develop document chunking techniques that preserve document structure
- Add metadata-aware retrieval to filter by document type, date, or other attributes
- Implement query decomposition for complex questions

### 3. Sentiment Analysis and Emotional Intelligence

**Challenge**: Add sentiment analysis to detect and respond appropriately to user emotions.

**Implementation Ideas**:
- Implement sentiment detection in user queries
- Adjust response tone based on detected sentiment
- Add specialized handling for frustrated or confused users
- Develop empathetic responses for sensitive topics
- Create a feedback loop to improve emotional intelligence over time

### 4. Integration with External Systems

**Challenge**: Connect the HR Assistant to external systems.

**Implementation Ideas**:
- Implement integration with HR management systems
- Add calendar integration for scheduling
- Create email notification capabilities
- Build integration with company document management systems
- Develop an API for third-party applications

## Conclusion

Through this capstone project, you've built Jenna, a sophisticated AI HR Assistant that combines multiple advanced NLP techniques to deliver a comprehensive HR support solution. You've implemented specialized RAG systems for both policy and benefits information, created a nuanced intent classification system, developed a conversation memory framework that maintains context across interactions, and orchestrated all components with LangGraph.

The completed system demonstrates how modern LLM applications can be enhanced with retrieval capabilities, specialized prompt engineering, and intelligent workflow orchestration. Your implementation handles sensitive workplace topics with appropriate care, manages multi-turn conversations effectively, and provides accurate information from a knowledge base of HR documents. These skills are directly applicable to real-world AI development scenarios, where contextual understanding, accurate information retrieval, and appropriate response generation are essential for building effective conversational AI systems.