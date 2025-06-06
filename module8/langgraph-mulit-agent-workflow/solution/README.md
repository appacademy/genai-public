# Customer Service Multi-Agent Workflow System

A modular, extensible system for processing customer service inquiries using specialized AI agents. The system classifies inquiries, routes them to the appropriate specialized handler, and generates personalized responses.

## Features

- **Multi-Agent Architecture**: Uses LangGraph to create a workflow of specialized agents
- **Intelligent Classification**: Automatically categorizes inquiries by type and priority
- **Specialized Handlers**: Dedicated handlers for billing, technical, product, and general inquiries
- **Priority Handling**: Special handling for urgent inquiries
- **Personalized Responses**: Customizes responses based on user information
- **AI Customer Support Representative**: Consistent identity (Emma G.) for all responses
- **Interactive Console**: User-friendly command-line interface
- **Demo Mode**: Built-in examples to showcase functionality
- **Robust Error Handling**: Graceful handling of API issues and edge cases
- **Enhanced JSON Extraction**: Multi-strategy approach for reliable classification

## Installation

1. Clone this repository
2. Copy the environment template file:
   ```bash
   cp .env.template .env
   ```
3. (Optional) Edit the `.env` file to configure your Ollama API URL
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Ensure you have Ollama running with the Gemma3:4b model available

## Usage

Run the application in interactive mode:
```bash
python app.py
```

Run the application in demo mode:
```bash
python app.py --demo
```

### Commands

- `exit`: Quit the application
- `help`: Display help information
- `clear`: Clear the screen
- `demo`: Run a demonstration with example inquiries

### User Information Format

You can include optional user information in your inquiries using the following format:
```
Your inquiry text [Name: Your Name, Email: your.email@example.com, Context: Additional details]
```

## Directory Structure

```
project/
├── models/          # Data models
│   └── state.py     # Message and AgentState TypedDict definitions
├── agents/          # Classification and routing logic
│   ├── classifier.py # Message classification
│   ├── router.py    # Message routing
│   └── handlers/    # Specialized inquiry handlers
│       ├── billing.py
│       ├── technical.py
│       ├── product.py
│       ├── general.py
│       └── priority.py
├── knowledge/       # Knowledge base functionality
│   └── knowledge_base.py
├── ui/              # User interface components
│   ├── console.py   # Interactive console interface
│   └── demo.py      # Demo functionality
├── utils/           # Utility functions
│   └── input_parser.py # User input parsing
├── workflow.py      # Workflow graph creation and execution
├── app.py           # Main entry point
├── ollama_client.py # Client for Ollama API
├── context/         # Knowledge base context files
│   ├── billing_context.json
│   ├── general_context.json
│   ├── priority_context.json
│   ├── product_context.json
│   └── technical_context.json
├── reference_docs/  # Documentation
│   └── _assets/
│       └── test-scenarios.md # Test scenarios
├── .env.template    # Template for environment configuration
└── requirements.txt # Dependencies
```

## Testing

The system includes a comprehensive set of test scenarios in `reference_docs/_assets/test-scenarios.md`. These scenarios cover different types of inquiries and expected behaviors, allowing you to verify that the system is functioning correctly.

## Dependencies

- langchain-core: Core components for LangChain
- langgraph: Graph-based workflow management
- requests: HTTP requests for API communication
- python-dotenv: Environment variable management
- re: Regular expression support for parsing

## LLM Integration

The system uses Ollama with the Gemma3:4b model by default. You can configure a different Ollama API URL in the `.env` file if needed.
