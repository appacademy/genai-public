# Jenna HR Assistant

Jenna is an AI-powered HR assistant designed to answer questions about company policies, benefits, and training programs.



## Features

* **Policy Q&A**: Get answers about company policies, PTO, work hours, etc.
* **Benefits Information**: Learn about available benefits, insurance, retirement plans, etc.
* **Training Management**: View, enroll in, and complete training courses
  * Course catalog with mandatory and elective courses
  * Training compliance status tracking
  * Automated renewal date calculation and notifications
  * Employee training history and snapshots
  * Enhanced record keeping with employee name tracking
* **Employee Data Management**: Centralized storage for employee information
  * HR representative access to employee and training data
  * Role-based access control for sensitive information
  * Bulk employee addition with automatic mandatory training enrollment (up to 10 employees at once)
* **Conversational Memory**: Maintains context across interactions with enhanced follow-up detection
* **Sensitivity Handling**: Special handling for sensitive topics like substance abuse and mental health
* **Continuous Conversation**: Maintains active session even when conversation flow is disrupted



## Setup

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Make sure you have Ollama installed and running with the required model:

```bash
ollama pull gemma3
```

3. Run the setup command to initialize the system:

```bash
python main.py setup
```



## Running the Application

To start the HR assistant:

```bash
python main.py start
```



## Document Management

The system includes several tools for document management:

* **Organize Documents**: `python main.py organize_documents`
* **Clean Up Duplicates**: `python main.py cleanup_documents`
* **Clean Up Library**: `python main.py cleanup_doc_library`



## Visualization and Analysis

The system includes tools for visualizing and analyzing conversation memory:

* **Memory Integration Tests**: `python test_memory_integration.py`
* **Visualization Tools**: `python visualize_memory.py`



## System Architecture

Jenna is built using a modular architecture:

* **Intent Classification**: Identifies the user's intent to route to appropriate handlers
* **RAG System**: Retrieves relevant documents and generates answers
* **Conversation Memory**: Tracks context and maintains state across interactions
* **Training Management**: Interfaces with training records for enrollment and tracking



## Memory System Integration

The memory system enhances Jenna's ability to maintain context across multiple interactions:

1. **Topic Detection**: Automatically classifies conversation topics
2. **Relevance Scoring**: Prioritizes the most important previous context
3. **Entity Tracking**: Identifies and tracks key entities mentioned in conversations
4. **Follow-up Detection**: Sophisticated detection of follow-up questions
5. **Context Organization**: Structures information for effective responses



## Development

This project uses LangGraph for workflow orchestration and LangChain for RAG components.



## HR Representative Access

The system includes a designated HR representative who has access to employee and training data:

* **HR Representative**: Jane Doe (Employee ID: E002)
* **Access Control**: Only the HR representative can view complete employee and training records
* **Authentication**: Verify as the HR representative by providing the correct name and employee ID
* **Available Commands**: 
  * "Show me all employees" - Display the employee directory
  * "Show me the training records" - Display the master training records
  * "Show training status for [employee name]" - Display training records for a specific employee
  * "Add these employees: E012 John Smith IT, E013 Jane Doe HR" - Add multiple employees at once
  * "Bulk add employees E014 Robert Jones Engineering and E015 Maria Garcia Marketing" - Another way to add employees in bulk
  * "Update employee E021 role to Department Manager" - Update an existing employee's information
  * "Change Emma Jackson's department to Operations" - Another way to update employee information
  * "How many people have completed HR-001?" - View analytics on course completion rates
  * "Show me department breakdown" - Get statistics on departmental distribution
  * "Which employees haven't finished SEC-010?" - List employees with incomplete courses
