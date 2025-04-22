# PromptLab

A workbench for designing, testing, and optimizing prompts for language models.

## Description

PromptLab is a Streamlit application that helps you create, test, and optimize prompts for language models. It provides a structured framework for prompt engineering, allowing you to:

- Create prompts using a five-part framework (context, instruction, response format, constraints, examples)
- Test prompts against various inputs and measure performance metrics
- Compare different prompt variations in A/B tests
- Analyze results with visualizations and get suggestions for improvement

The application uses Ollama to run local LLMs, so there's no need for API keys or worrying about rate limits.

## Features

- **Structured Prompt Creation**: Build prompts using the five-part framework
- **Prompt Testing**: Test prompts with different inputs and get performance metrics
- **A/B Testing**: Compare different prompt variations side-by-side
- **Results Analysis**: Visualize metrics and get improvement suggestions
- **Local Model Integration**: Works with Ollama for using open-source LLMs locally

## Requirements

- Python 3.8 or higher
- Ollama installed with models (recommended: gemma:3-4b)

## Installation

1. Clone the repository
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running with at least one model installed (e.g., gemma:3-4b)

## Usage

1. Start the Streamlit app:

```bash
cd promptlab
streamlit run app.py
```

2. The app will open in your browser at http://localhost:8501
3. Use the sidebar to navigate between different sections:
   - Create Prompt: Design new prompt templates
   - Test Prompt: Test prompts against various inputs
   - A/B Testing: Compare different prompt variations
   - Results Analysis: Review test results and get suggestions

## Workflow

1. **Create a prompt template** using the five-part framework
2. **Test the prompt** with different inputs to see how it performs
3. **Create variations** of your prompt to try different approaches
4. **Compare variations** in A/B tests to see which performs better
5. **Analyze the results** and get suggestions for improvement
6. **Refine your prompt** based on the insights and repeat

## How It Works

PromptLab uses the following components:

- **PromptTemplate**: Represents a prompt structured in five parts
- **PromptTest**: Handles testing prompts against inputs and calculating metrics
- **PromptLab**: The main workbench that combines templates, tests, and results
- **OllamaService**: Connects to Ollama to run local language models
