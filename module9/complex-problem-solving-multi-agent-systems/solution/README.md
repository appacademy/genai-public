# Multi-Agent Problem Solving System

A framework for solving complex problems using a coordinated network of specialized AI agents with LangGraph workflow orchestration.

## Overview

This system uses multiple specialized agents to break down and solve complex problems:

1. **Research Agent**: Gathers key information about the problem
2. **Analysis Agent**: Identifies core issues and relationships
3. **Solution Agent**: Proposes comprehensive solutions
4. **Review Agent**: Critically evaluates proposed solutions

The agents work together in a coordinated workflow, with each agent building upon the work of the previous agents. The system uses LangGraph to manage the workflow and state transitions between agents.

## Features

- **LangGraph Workflow**: Directed graph-based agent orchestration
- **Specialized Agents**: Each focused on a specific aspect of problem-solving
- **Markdown Reports**: Detailed documentation of the problem-solving process
- **Interactive Mode**: Solve your own custom problems
- **Demo Mode**: Try the system with a pre-defined problem

## Requirements

- Python 3.9+
- [Ollama](https://ollama.ai/) with the `gemma3:4b` model (or another compatible model)

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.template .env
   ```
4. If needed, edit the `.env` file to update the `OLLAMA_API_URL` with your Ollama server URL

## Usage

Run the application:
```bash
python app.py
```

### Menu Options

1. **Run Demo**: Solve a pre-defined problem about employee retention
2. **Interactive Problem Solving**: Input your own problem to solve
3. **Exit**: Quit the application

### Output

For each problem, the system will:
1. Generate a detailed solution through multiple agent interactions
2. Display the final solution in the console
3. Save a comprehensive markdown report to the `outputs` directory

## Architecture

The system consists of several key components:

- **Agent Framework** (`agents/base_agent.py`): Abstract base class for all agents
- **Specialized Agents**: Research, Analysis, Solution, and Review agents
- **LangGraph Workflow** (`workflows/graph_workflow.py`): Orchestrates agent interactions
- **Markdown Writer** (`utils/markdown_writer.py`): Generates detailed reports
- **Ollama Client** (`utils/ollama_client.py`): Handles LLM communication

## Current Limitations

- Limited to a maximum of 2 iterations for solution refinement
- Requires a running Ollama instance with appropriate models
- Processing time depends on the local LLM used

## Example Problems

The system can handle a wide range of complex problems, including:

- Business strategy challenges
- Organizational development issues
- Product development planning
- Community and social initiatives
- Personal development and productivity

## License

[MIT License](LICENSE)
