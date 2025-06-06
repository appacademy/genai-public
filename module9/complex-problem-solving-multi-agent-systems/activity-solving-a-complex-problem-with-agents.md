# Activity: Solving a Complex Problem with Agents



## Overview

In this hands-on coding activity, we'll build a collaborative multi-agent system where specialized LLM agents work together to solve complex analytical problems. The system decomposes problems hierarchically, with different agents handling specific phases: research, analysis, solution generation, and critical review. we'll implement a LangGraph workflow that orchestrates these agents, manages state transitions, and enables iterative solution refinement. This approach mirrors real-world complex problem-solving scenarios where different expertise must be coordinated effectively to tackle challenging problems that would be difficult for a single agent to solve.



## Learning Objectives

By completing this activity, you will be able to:
1. Design a multi-agent architecture using hierarchical decomposition for complex problem-solving
2. Implement role-based task allocation with specialized agents that have clear responsibilities
3. Develop effective communication protocols between agents to share information and coordinate results
4. Create adaptive feedback loops that improve solution quality through critical review and iteration
5. Apply LangGraph to orchestrate a complete problem-solving workflow with LLM agents



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
langchain-community==0.3.20
python-dotenv==1.0.0
pydantic==2.7.4
requests==2.32.3
langgraph>=0.1.0
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

The problem-solving system uses a multi-agent architecture with several key components:

1. **Research Agent**: Gathers key information about the problem, identifies relevant facts, context, and potential resources

2. **Analysis Agent**: Processes research findings to identify core issues, relationships between facts, and potential approaches

3. **Solution Agent**: Proposes comprehensive solutions based on the research and analysis, structured as actionable plans

4. **Critical Review Agent**: Evaluates proposed solutions, identifies strengths and weaknesses, and provides feedback for improvement

### LangGraph Workflow Management

The system uses LangGraph to create a directed graph that orchestrates the flow of information:

1. **Nodes**: Each agent or processing step is represented as a node in the graph
2. **Edges**: Define the possible transitions between nodes
3. **Conditional Routing**: Solutions follow different paths through the graph based on the review recommendation
4. **State Management**: The workflow maintains consistent state as information progresses through the system

### Problem-Solving Process

The system uses a structured process for solving complex problems:

1. **Research Phase**: Gathers key facts, context, and resources related to the problem
2. **Analysis Phase**: Identifies core issues, relationships, and potential approaches
3. **Solution Phase**: Develops a comprehensive, actionable solution plan
4. **Review Phase**: Critically evaluates the solution and provides feedback
5. **Iteration**: If needed, the solution is refined based on the review feedback

### Report Generation

The system generates detailed markdown reports that document the entire problem-solving process:

1. **Problem Statement**: The original problem description
2. **Research Findings**: Key facts, context, and resources identified
3. **Analysis**: Core issues, relationships, and potential approaches
4. **Solution**: The proposed solution plan
5. **Review**: Critical evaluation of the solution
6. **Final Solution**: The refined solution after iteration (if applicable)

Each report is comprehensive, typically around 3,000 words, and captures the complete thought process of each agent. The application automatically saves the contents of the terminal window to a markdown file in the outputs directory, providing a detailed record of the problem-solving process that can be reviewed later or shared with others.

## LangGraph Framework

This activity uses the LangGraph framework to orchestrate the workflow. LangGraph is built on top of LangChain and provides powerful tools for creating directed graphs of components that can be connected together to form complex workflows.

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
                     │  Research   │
                     │   Agent     │
                     │             │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │             │
                     │  Analysis   │
                     │   Agent     │
                     │             │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │             │
                     │  Solution   │
                     │   Agent     │
                     │             │
                     └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
                     │             │
                     │   Review    │
                     │   Agent     │
                     │             │
                     └──────┬──────┘
                            │
           ┌────────────────┴────────────────┐
           │                                 │
           ▼                                 ▼
    ┌─────────────┐                   ┌─────────────┐
    │             │                   │             │
    │  Solution   │                   │    End      │
    │   Agent     │                   │    Node     │
    │ (Iteration) │                   │             │
    └──────┬──────┘                   └─────────────┘
           │                                 ▲
           │                                 │
           └─────────────────────────────────┘
```



## Activity Tasks

In this activity, we'll implement several key components of the Multi-Agent Problem Solving system by completing the TODO items in the starter code. Each task focuses on an important aspect of building a LangGraph-based workflow for complex problem-solving.

### Task 1: Study the Research Agent

Your first task is to thoroughly examine the implemented research agent in the `agents/research_agent.py` file. This example demonstrates how to build an effective LLM-powered agent within our system architecture. By analyzing this reference implementation, we'll learn the essential patterns needed for the agents we'll build in subsequent tasks.

The research agent demonstrates four key components that are fundamental to all agents in our system:

1. **Input Extraction**: Notice how the agent extracts the problem from the input dictionary using `inputs.get("problem", "")`. This pattern safely retrieves input values with a default if the key doesn't exist.
   
2. **System Prompt Construction**: The agent creates a well-structured system prompt that provides clear instructions to the LLM. This prompt defines the agent's role ("specialized research agent"), purpose ("gathering key information"), and expected output format (structured sections for Key Facts, Contextual Information, Potential Resources, and Initial Hypotheses).
   
```python
# System Prompt Construction
        system_prompt = """
        You are a specialized research agent responsible for gathering key information about a problem.
        Your goal is to identify:
        1. Key facts relevant to the problem
        2. Important context or background information
        3. Potential resources or references that might help solve the problem
        
        Provide your research in a clear, structured format with sections for:
        - Key Facts
        - Contextual Information
        - Potential Resources
        - Initial Hypotheses
        """

        user_prompt = f"I need you to research the following problem: {problem}"
```
   
3. **LLM Interaction**: The agent calls the LLM by invoking the `_call_llm()` method with both the system prompt and a user prompt that incorporates the problem. This separation maintains clean boundaries between instructions and user input.
   
4. **Response Formatting**: Finally, the agent returns an `AgentResponse` object with properly structured output, including the LLM's response content, a confidence score, and relevant metadata that provides traceability.
   
```python
# Response Formatting
return AgentResponse(
	content=research_results,
	confidence=0.8,
	metadata={"source": "research_agent", "problem": problem},
)
```
   

Pay particular attention to how the system prompt guides the LLM to produce organized, section-based output—this pattern will be essential when implementing the remaining agents. No coding is required for this task, but understanding these implementation patterns will serve as your blueprint for Tasks 2-4.


### Task 2: Implement the Analysis Agent

For this task, we'll implement the analysis agent in the `agents/analysis_agent.py` file by implementing the `process` method. The analysis agent is the second step in our workflow and receives the research results from the research agent. Its role is to transform raw research data into structured analytical insights. 

Our implementation will extract both the problem statement and research results from the input dictionary and pass them to the LLM. The system prompt directs the LLM to perform four key analytical functions: 

1. identify and prioritize core issues within the problem, 
2. explore relationships and dependencies between different pieces of information, 
3. evaluate potential approaches to solving the problem, and 
4. recommend specific focus areas for the solution. 

The user prompt includes the problem and research results. When we call the LLM, 
an `AgentResponse` with a confidence score of 0.7 is returned, reflecting the inherent uncertainty in analytical work. This task demonstrates how agents can build upon each other's outputs to progressively refine information.

   **Step 2.1**. Find the TODO comment: "Implement the process method that:" and follow the steps below.

   **Step 2.2**. Find the TODO comment: "Extract problem and research_results from the inputs dictionary" and add this code snippet:

   ```python
    problem = inputs.get("problem", "")
    research_results = inputs.get("research_results", "")
   ```

   This code extracts the problem statement and research results from the input dictionary, using empty strings as default values if these keys are not present.

   **Step 2.3**. Find the TODO comment: "Define the system prompt for the analysis agent" and add this code snippet:

   ```python
    system_prompt = """
    You are a specialized analysis agent. Your job is to process research findings and identify:
    1. Core issues within the problem
    2. Relationships between different aspects of the problem
    3. Potential approaches to solving the problem
    4. Priority areas to address
    
    Structure your analysis with the following sections:
    - Core Issues (prioritized)
    - Relationships and Dependencies
    - Potential Approaches
    - Recommended Focus Areas
    """
   ```

   This code defines the system prompt that instructs the LLM on its role as an analysis agent and how to structure its output with four key analytical sections.

   **Step 2.4**. Find the TODO comment: "Create a user prompt that includes the problem and research results" and add this code snippet:

   ```python
    user_prompt = f"""
    Problem: {problem}
    
    Research Results:
    {research_results}
    
    Please analyze this information and provide your insights.
    """
   ```

   This code creates a formatted user prompt that includes the problem statement and research results, instructing the LLM to analyze the information.

   **Step 2.5**. Find the TODO comment: "Call the LLM using self._call_llm" and add this code snippet:

   ```python
    analysis_results = self._call_llm(system_prompt, user_prompt)
   ```

   This code calls the LLM with both the system prompt (which directs the LLM on how to structure its analysis) and the user prompt (which contains the problem and research data).

   **Step 2.6**. Find the TODO comment: "Return an AgentResponse with the analysis results, confidence score, and metadata" and add this code snippet:

   ```python
    return AgentResponse(
        content=analysis_results,
        confidence=0.7,
        metadata={"source": "analysis_agent"},
    )
   ```

   This code returns an AgentResponse object containing the analysis results from the LLM, a confidence score of 0.7 (reflecting the inherent uncertainty in analytical work), and metadata identifying the source as the analysis agent.


### Task 3: Implement the Solution Agent

In this task, we'll implement the solution agent in the `agents/solution_agent.py` file. This agent represents the creative problem-solving phase of our workflow. It takes inputs from both the research and analysis phases to propose comprehensive solutions. 

Our implementation must handle four input parameters: 
1. the problem statement, 
2. research results, 
3. analysis results, 
4. and any previous critique (which will be present during iteration). 

The system prompt guides the LLM to develop a detailed, actionable solution with an executive summary, proposed solutions with rationales, implementation steps, expected outcomes, potential challenges, and success metrics. 

A user prompt collects all the extracted information before the LLM is called. 

A key feature of this agent is its adaptive behavior—we implement adaptive confidence scoring that increases from 0.75 for initial solutions to 0.9 for refined solutions, reflecting the increased certainty that comes with iteration. This task demonstrates how to create agents that adapt their behavior based on workflow context.

   **Step 3.1**. Find the TODO comment: "Implement the process method that:" and follow the steps below.

   **Step 3.2**. Find the TODO comment: "Extract all required inputs from the inputs dictionary" and add this code snippet:

   ```python
    problem = inputs.get("problem", "")
    research_results = inputs.get("research_results", "")
    analysis_results = inputs.get("analysis_results", "")
    previous_critique = inputs.get("previous_critique", "")
   ```

   This code extracts the problem statement, research results, analysis results, and any previous critique from the inputs dictionary, using empty strings as default values if any of these inputs are missing.

   **Step 3.3**. Find the TODO comment: "Define the system prompt" and add this code snippet:

   ```python
    system_prompt = """
    You are a specialized solution generation agent. Your job is to propose comprehensive 
    solutions to the problem based on research and analysis.
    
    Create a detailed solution with the following components:
    1. Executive Summary
    2. Proposed Solutions (with rationale for each)
    3. Implementation Steps
    4. Expected Outcomes
    5. Potential Challenges
    6. Success Metrics
    
    If you've received previous critique, make sure to address those points in your updated solution.
    """
   ```

   This code defines the system prompt that guides the LLM to develop a detailed, actionable solution with specific components including an executive summary, proposed solutions with rationales, implementation steps, expected outcomes, potential challenges, and success metrics.

   **Step 3.4**. Find the TODO comment: "Create a user prompt that includes all the extracted information" and add this code snippet:

   ```python
    user_prompt = f"""
    Problem: {problem}
    
    Research Results:
    {research_results}
    
    Analysis:
    {analysis_results}
    
    Previous Critique (if any):
    {previous_critique}
    
    Please generate a comprehensive solution to this problem.
    """
   ```

   This code creates a user prompt that includes all the extracted information: the problem statement, research results, analysis results, and any previous critique, formatted in a clear and structured way.

   **Step 3.5**. Find the TODO comment: "Call the LLM using self._call_llm" and add this code snippet:

   ```python
    solution = self._call_llm(system_prompt, user_prompt)
   ```

   This code calls the LLM with the system prompt and user prompt to generate a solution.

   **Step 3.6**. Find the TODO comment: "Implement adaptive confidence scoring based on whether this is an iteration" and add this code snippet:

   ```python
    # Adjust confidence based on whether this is an iteration after critique
    confidence = 0.9 if previous_critique else 0.75
   ```

   This code implements adaptive confidence scoring that increases from 0.75 for initial solutions to 0.9 for refined solutions (when there's a previous critique), reflecting the increased certainty that comes with iteration.

   **Step 3.7**. Find the TODO comment: "Return an AgentResponse with the solution, confidence score, and metadata" and add this code snippet:

   ```python
    return AgentResponse(
        content=solution,
        confidence=confidence,
        metadata={
            "source": "solution_agent",
            "iteration": 1 if not previous_critique else 2,
        },
    )
   ```

   This code returns an AgentResponse object containing the solution content, the calculated confidence score, and metadata that includes the source of the response and the iteration number (1 for initial solutions, 2 for refined solutions).



### Task 4: Implement the Critical Review Agent

In Task 4, we'll implement the critical review agent in the `agents/review_agent.py` file. This agent creates the feedback loop in our system, evaluating proposed solutions and determining whether they need further refinement. 

Our implementation should extract all relevant information from the inputs (problem, research, analysis, and proposed solution) and pass them to the LLM for evaluation. 

The system prompt directs the LLM to:

1. assess both strengths and weaknesses of the solution, 
2. identify gaps or inconsistencies, 
3. suggest improvements, 
4. and provide a clear recommendation.  

The user prompt will collect all the extracted information and then we call the LLM. 

A key technical challenge is extracting the recommendation ("Accept", "Revise", or "Reject") from the LLM's response. We'll implement logic that searches for these keywords in the response and stores them in the metadata. The recommendation determines the workflow path, making this agent critical for the adaptive behavior of the entire system. This task demonstrates how agents can make decisions that affect the control flow of a multi-agent system.

   **Step 4.1**. Find the TODO comment: "Extract all required inputs from the inputs dictionary" and add this code snippet:

   ```python
    problem = inputs.get("problem", "")
    research_results = inputs.get("research_results", "")
    analysis_results = inputs.get("analysis_results", "")
    proposed_solution = inputs.get("proposed_solution", "")
   ```

   This code extracts the problem statement, research results, analysis results, and proposed solution from the inputs dictionary, using empty strings as default values if any of these keys are missing.

   **Step 4.2**. Find the TODO comment: "Define the system prompt for the critical review agent" and add this code snippet:

   ```python
    system_prompt = """
    You are a specialized critical review agent. Your job is to carefully evaluate 
    proposed solutions and identify:
    
    1. Gaps or missing considerations
    2. Logical inconsistencies
    3. Implementation challenges
    4. Alternative approaches that might be superior
    5. Strengths of the current solution
    
    Be constructive but thorough in your critique. Structure your review with:
    - Solution Strengths
    - Critical Gaps
    - Inconsistencies
    - Implementation Concerns
    - Suggested Improvements
    
    End with an overall assessment and a clear recommendation: 
    Accept, Revise, or Reject the proposed solution.
    """
   ```

   This code defines the system prompt that instructs the LLM on its role as a critical review agent, including what aspects to evaluate and how to structure its response.

   **Step 4.3**. Find the TODO comment: "Create a user prompt that includes all the extracted information" and add this code snippet:

   ```python
    user_prompt = f"""
    Problem: {problem}
    
    Research Results:
    {research_results}
    
    Analysis:
    {analysis_results}
    
    Proposed Solution:
    {proposed_solution}
    
    Please provide a critical review of this solution.
    """
   ```

   This code creates a formatted user prompt that includes all the extracted information in a structured format, making it clear to the LLM what it needs to review.

   **Step 4.4**. Find the TODO comment: "Call the LLM using self._call_llm" and add this code snippet:

   ```python
    critique = self._call_llm(system_prompt, user_prompt)
   ```

   This code calls the language model with both the system prompt (which defines the agent's role) and the user prompt (which contains the specific information to review).

   **Step 4.5**. Find the TODO comment: "Extract recommendation using a simple heuristic" and add this code snippet:

   ```python
    recommendation = "Revise"  # Default
    if "Accept" in critique[-100:]:
        recommendation = "Accept"
    elif "Reject" in critique[-100:]:
        recommendation = "Reject"
   ```

   This code extracts the recommendation from the critique by looking for the keywords "Accept" or "Reject" in the last 100 characters of the response. If neither is found, it defaults to "Revise".

   **Step 4.6**. Find the TODO comment: "Return an AgentResponse with the critique, confidence score, and metadata" and add this code snippet:

   ```python
    return AgentResponse(
        content=critique,
        confidence=0.85,
        metadata={
            "source": "critical_review_agent",
            "recommendation": recommendation,
        },
    )
   ```

   This code returns an AgentResponse object containing the critique content, a confidence score of 0.85, and metadata that includes the source of the response and the extracted recommendation.


### Task 5: Implement the LangGraph Workflow

In this task, we'll implement the LangGraph workflow that orchestrates all agents in the `workflows/graph_workflow.py` file. This is where the individual agents come together to form a cohesive problem-solving system. 

We'll implement all four agent functions (`run_research`, `run_analysis`, `run_solution`, and `run_review`) that serve as wrappers around the agents, handling state management and markdown report generation. Each function will extract the necessary information from the state, call the appropriate agent, update the markdown writer with the results, and return a dictionary with the updated state values. 

Next, we'll implement the `should_continue` function that creates the adaptive feedback loop, determining whether to perform another solution iteration or end the workflow based on the review recommendation and iteration count. 

Then, we'll implement the `build_problem_solving_graph` function that constructs the complete StateGraph with all nodes and edges, defines the workflow's structure, and implements conditional routing. 

Finally, we'll implement the `solve_problem_with_graph` function that serves as the main entry point for our workflow. This function initializes the markdown writer for documentation, builds the problem-solving graph, creates the initial state with the problem statement, executes the graph with appropriate recursion settings, and processes the results. It organizes all outputs into a comprehensive results dictionary containing the complete problem-solving journey—from initial research to the final solution—and saves a formatted markdown report detailing the entire process.

This task demonstrates how to orchestrate multiple specialized agents into a unified system using LangGraph's directed graph capabilities.

1. Implement the LangGraph Workflow, starting with the `run_research` function.

    **Step 5.1**. Find the TODO comment: "Implement the run_research function" and follow the steps below.
    
    **Step 5.2**. Find the TODO comment: "1. Print a message indicating the Research Agent is working" and add this code snippet:
    
    ```python
    print("📚 Research Agent working...")
    ```
    
    This code prints a message to indicate that the Research Agent is now working on the problem.
    
    **Step 5.3**. Find the TODO comment: "2. Extract the problem from the state" and add this code snippet:
    
    ```python
    problem = state.problem
    ```
    
    This code extracts the problem from the current state object for processing.
    
    **Step 5.4**. Find the TODO comment: "3. Call the research_agent with the problem" and add this code snippet:
    
    ```python
    response = research_agent.process({"problem": problem})
    ```
    
    This code calls the research_agent with the problem and stores the response.
    
    **Step 5.5**. Find the TODO comment: "4. Print the confidence score of the response" and add this code snippet:
    
    ```python
    print(f"Research complete with confidence: {response.confidence:.2f}\n")
    ```
    
    This code prints the confidence score of the research agent's response, formatted to two decimal places.
    
    **Step 5.6**. Find the TODO comment: "5. Add the research results to the markdown writer" and add this code snippet:
    
    ```python
    # Add to markdown
    if markdown_writer:
        markdown_writer.add_section("Research Phase", response.content)
    ```
    
    This code adds the research results to the markdown writer if it exists, creating a section titled "Research Phase".
    
    **Step 5.7**. Find the TODO comment: "6. Return a dictionary with the research_results key" and add this code snippet:
    
    ```python
    return {"research_results": response.content}
    ```
    
    This code returns a dictionary containing the research results, which will be used in the next steps of the workflow.


2. Define the `run_analysis` agent function for the graph state

    **Step 5.8**. Find the TODO comment: "Implement the run_analysis function" and follow the steps below.
    
    **Step 5.9**. Find the TODO comment: "Print a message indicating the Analysis Agent is working" and add this code snippet:
    
    ```python
    print("🧩 Analysis Agent working...")
    ```
    
    This code prints a message to indicate that the Analysis Agent has started working.
    
    **Step 5.10**. Find the TODO comment: "Extract the problem and research_results from the state" and add this code snippet:
    
    ```python
    problem = state.problem
    research_results = state.research_results
    ```
    
    This code extracts the problem description and research results from the current state object.
    
    **Step 5.11**. Find the TODO comment: "Call the analysis_agent with the problem and research_results" and add this code snippet:
    
    ```python
    response = analysis_agent.process(
        {"problem": problem, "research_results": research_results}
    )
    ```
    
    This code calls the analysis_agent with the problem and research results, which will analyze the information and return a response.
    
    **Step 5.12**. Find the TODO comment: "Print the confidence score of the response" and add this code snippet:
    
    ```python
    print(f"Analysis complete with confidence: {response.confidence:.2f}\n")
    ```
    
    This code prints the confidence score of the analysis response, formatted to two decimal places.
    
    **Step 5.13**. Find the TODO comment: "Add the analysis results to the markdown writer" and add this code snippet:
    
    ```python
    # Add to markdown
    if markdown_writer:
        markdown_writer.add_section("Analysis Phase", response.content)
    ```
    
    This code adds the analysis results to the markdown writer as a new section titled "Analysis Phase", but only if the markdown_writer exists.
    
    **Step 5.14**. Find the TODO comment: "Return a dictionary with the analysis_results key" and add this code snippet:
    
    ```python
    return {"analysis_results": response.content}
    ```
    
    This code returns a dictionary containing the analysis results, which will be added to the state for use in subsequent steps of the workflow.


3. Implement the `run_solution` agent function for the graph state.

    **Step 5.15**. Find the TODO comment: "Implement the run_solution function" and follow the steps below.
    
    **Step 5.16**. Find the TODO comment: "1. Print a message indicating the Solution Agent is working" and add this code snippet:
    
    ```python
    iteration = state.iteration
    print(f"💡 Solution Agent working (iteration {iteration})...")
    ```
    
    This code retrieves the current iteration number from the state and prints a message indicating that the Solution Agent is working on this iteration.
    
    **Step 5.17**. Find the TODO comment: "2. Extract the problem, research_results, analysis_results, and critique from the state" and add this code snippet:
    
    ```python
    problem = state.problem
    research_results = state.research_results
    analysis_results = state.analysis_results
    previous_critique = state.critique
    ```
    
    This code extracts all the necessary information from the state object that will be needed for the solution agent to generate a solution.
    
    **Step 5.18**. Find the TODO comment: "3. Call the solution_agent with all the extracted information" and add this code snippet:
    
    ```python
    response = solution_agent.process(
        {
            "problem": problem,
            "research_results": research_results,
            "analysis_results": analysis_results,
            "previous_critique": previous_critique,
        }
    )
    ```
    
    This code calls the solution agent with all the extracted information packaged as a dictionary, allowing the agent to process the problem and generate a solution.
    
    **Step 5.19**. Find the TODO comment: "4. Print the confidence score of the response" and add this code snippet:
    
    ```python
    print(f"Solution generated with confidence: {response.confidence:.2f}\n")
    ```
    
    This code prints the confidence score of the solution generated by the agent, formatted to two decimal places.
    
    **Step 5.20**. Find the TODO comment: "5. Add the solution to the markdown writer" and add this code snippet:
    
    ```python
    # Add to markdown
    if markdown_writer:
        # Simplify heading if there's only one iteration
        if iteration == 1:
            section_title = "Solution Phase"
        else:
            section_title = f"Solution Phase (Iteration {iteration})"

        markdown_writer.add_section(section_title, response.content)
    ```
    
    This code adds the solution to the markdown writer with an appropriate section title. If it's the first iteration, it uses "Solution Phase" as the title; otherwise, it includes the iteration number.
    
    **Step 5.21**. Find the TODO comment: "6. Return a dictionary with the solution key" and add this code snippet:
    
    ```python
    return {"solution": response.content}
    ```
    
    This code returns a dictionary with the solution content, which will be used by the LangGraph workflow to update the state.


4. Define the agent functions that work with the graph state.

    **Step 5.22**. Find the TODO comment: "Implement the run_review function" and follow the steps below.
    
    **Step 5.23**. Find the TODO comment: "Print a message indicating the Critical Review Agent is evaluating the solution" and add this code snippet:
    
    ```python
    print(f"🔍 Critical Review Agent evaluating solution...")
    ```
    
    This code prints a message to indicate that the Critical Review Agent is starting its evaluation process.
    
    **Step 5.24**. Find the TODO comment: "Extract the problem, research_results, analysis_results, and solution from the state" and add this code snippet:
    
    ```python
    problem = state.problem
    research_results = state.research_results
    analysis_results = state.analysis_results
    solution = state.solution
    ```
    
    This code extracts all the necessary information from the state object that will be needed for the review process.
    
    **Step 5.25**. Find the TODO comment: "Call the review_agent with all the extracted information" and add this code snippet:
    
    ```python
    response = review_agent.process(
        {
            "problem": problem,
            "research_results": research_results,
            "analysis_results": analysis_results,
            "proposed_solution": solution,
        }
    )
    ```
    
    This code calls the review_agent with all the extracted information packaged as a dictionary, allowing the agent to process and evaluate the solution.
    
    **Step 5.26**. Find the TODO comment: "Extract the recommendation from the response metadata" and add this code snippet:
    
    ```python
    recommendation = response.metadata.get("recommendation", "Revise")
    ```
    
    This code extracts the recommendation from the response metadata, with a default value of "Revise" if no recommendation is found.
    
    **Step 5.27**. Find the TODO comment: "Print the recommendation" and add this code snippet:
    
    ```python
    print(f"Review complete - Recommendation: {recommendation}\n")
    ```
    
    This code prints the recommendation that was extracted from the response metadata.
    
    **Step 5.28**. Find the TODO comment: "Add the critique to the markdown writer" and add this code snippet:
    
    ```python
    # Add to markdown
    if markdown_writer:
        markdown_writer.add_section("Review Phase", response.content)
    ```
    
    This code adds the critique content to the markdown writer if it exists, creating a section titled "Review Phase".
    
    **Step 5.29**. Find the TODO comment: "Return a dictionary with the critique and recommendation keys" and add this code snippet:
    
    ```python
    return {"critique": response.content, "recommendation": recommendation}
    ```
    
    This code returns a dictionary containing the critique content and the recommendation, which will be used by the workflow to determine next steps.



5. Implement the `should_continue` function that creates the adaptive feedback loop.

    **Step 5.30**. Find the TODO comment: "Implement the should_continue function that creates the adaptive feedback loop" and follow the steps below.
    
    **Step 5.31**. Find the TODO comment: "Implement the should_continue function" and add this code snippet:
    
    ```python
    recommendation = state.recommendation
    iteration = state.iteration

    # Strict termination after exactly 1 iteration (which means 2 total iterations since we start at 1)
    if recommendation == "Accept" or iteration >= 1:
        # Final solution is the current solution
        print(
            f"✅ Problem solving complete after {iteration + 1} iterations! Final recommendation: {recommendation}"
        )
        return "end_node"
    else:
        # Increment iteration counter
        print(f"⟳ Starting iteration {iteration + 1} (final iteration)...")
        return "solution_node"
    ```
    
    This code extracts the recommendation and iteration count from the state. It then determines whether to continue with another solution iteration or end the workflow. If the recommendation is "Accept" or the iteration count is greater than or equal to 1, it prints a completion message and returns "end_node". Otherwise, it prints a message about starting the next iteration and returns "solution_node" to continue the workflow.


6. Implement the build_problem_solving_graph function.

    **Step 5.32**. Find the TODO comment: "Implement the build_problem_solving_graph function" and follow the steps below.
    
    **Step 5.33**. Find the TODO comment: "Create a new StateGraph with the ProblemSolvingState type" and add this code snippet:
    
    ```python
    # Create a new graph
    workflow = StateGraph(ProblemSolvingState)
    ```
    
    This code initializes a new StateGraph object with the ProblemSolvingState type that will be used to define our workflow.
    
    **Step 5.34**. Find the TODO comment: "Add all the agent nodes (research, analysis, solution_node, review, end_node)" and add this code snippet:
    
    ```python
    # Add all the agent nodes
    workflow.add_node("research", run_research)
    workflow.add_node("analysis", run_analysis)
    workflow.add_node("solution_node", run_solution)
    workflow.add_node("review", run_review)
    workflow.add_node("end_node", lambda x: x)  # Identity function as a terminal node
    ```
    
    This code adds five nodes to our workflow graph, each representing a different step in the problem-solving process. The "end_node" uses a simple identity function that returns its input unchanged.
    
    **Step 5.35**. Find the TODO comment: "Add the edges to connect the nodes in the correct sequence" and add this code snippet:
    
    ```python
    # Add the edges - how the agents connect to each other
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "analysis")
    workflow.add_edge("analysis", "solution_node")
    workflow.add_edge("solution_node", "review")
    ```
    
    This code connects the nodes in sequence, defining the flow from the START node through research, analysis, solution, and finally to the review node.
    
    **Step 5.36**. Find the TODO comment: "Add conditional edges based on the should_continue function" and add this code snippet:
    
    ```python
    workflow.add_conditional_edges("review", should_continue)
    workflow.add_edge("end_node", END)
    ```
    
    This code adds a conditional edge from the review node that uses the should_continue function to determine the next step. It also connects the end_node to the END state of the workflow.
    
    **Step 5.37**. Find the TODO comment: "Compile and return the graph" and add this code snippet:
    
    ```python
    # Compile the graph
    return workflow.compile()
    ```
    
    This code compiles the workflow graph, which prepares it for execution, and returns the compiled graph.

---

7. Implement the `solve_problem_with_graph` function, which serves as the main entry point for our workflow..

    **Step 5.38**. Find the TODO comment: "Implement the solve_problem_with_graph function" and follow the steps below.
    
    **Step 5.39**. Find the TODO comment: "Initialize the markdown writer with the problem statement" and add this code snippet:
    
    ```python
    global markdown_writer

    # Initialize markdown writer
    markdown_writer = MarkdownWriter(problem)
    ```
    
    This code creates a global markdown writer object that will be used to generate a report of the problem-solving process.
    
    **Step 5.40**. Find the TODO comment: "Build the problem-solving graph if not already initialized" and add this code snippet:
    
    ```python
    # Initialize graph if not already done
    graph = build_problem_solving_graph()
    ```
    
    This code calls the `build_problem_solving_graph` function to create the LangGraph workflow if it hasn't been created yet.
    
    **Step 5.41**. Find the TODO comment: "Create the initial state with the problem and set iteration to 1" and add this code snippet:
    
    ```python
    # Initial state
    initial_state = ProblemSolvingState(problem=problem, iteration=1)
    ```
    
    This code creates the initial state object that will be passed to the graph, containing the problem statement and setting the iteration counter to 1.
    
    **Step 5.42**. Find the TODO comment: "Print a message indicating the problem-solving process is starting" and add this code snippet:
    
    ```python
    print(f"🔍 Starting to solve problem: {problem[:50]}...\n")
    ```
    
    This code prints a message to the console showing the first 50 characters of the problem to indicate that the solving process has begun.
    
    **Step 5.43**. Find the TODO comment: "Execute the graph with appropriate recursion limit settings" and add this code snippet:
    
    ```python
    # Execute the graph with increased recursion limit
    result = graph.invoke(initial_state, {"recursion_limit": 50})
    ```
    
    This code runs the LangGraph workflow by invoking the graph with the initial state and setting a recursion limit of 50 to allow for multiple iterations.
    
    **Step 5.44**. Find the TODO comment: "Add the final solution to the markdown report" and add this code snippet:
    
    ```python
    # Add final solution to markdown
    if result.get("final_solution"):
        markdown_writer.add_section("Final Solution", result.get("final_solution", ""))
    else:
        markdown_writer.add_section("Final Solution", result.get("solution", ""))
    ```
    
    This code adds the final solution to the markdown report, using either the "final_solution" field if available or falling back to the "solution" field.
    
    **Step 5.45**. Find the TODO comment: "Save the markdown report to a file and print the output path" and add this code snippet:
    
    ```python
    # Save markdown to file
    output_path = markdown_writer.save()
    print(f"\n✅ Markdown report saved to: {output_path}")
    ```
    
    This code saves the markdown report to a file and prints the file path to the console.
    
    **Step 5.46**. Find the TODO comment: "Format and return the results dictionary with all components" and add this code snippet:
    
    ```python
    # Format the output similar to the orchestrator for compatibility
    formatted_result = {
        "problem": problem,
        "research": result.get("research_results", ""),
        "analysis": result.get("analysis_results", ""),
        "solution_history": [
            {
                "iteration": i + 1,
                "solution": result.get("solution", ""),
                "critique": result.get("critique", ""),
                "recommendation": result.get("recommendation", ""),
            }
            for i in range(result.get("iteration", 1))
        ],
        "final_solution": result.get("final_solution", ""),
        "final_critique": result.get("critique", ""),
        "recommendation": result.get("recommendation", ""),
        "markdown_path": output_path,
    }

    return formatted_result
    ```
    
    This code creates a dictionary containing all the components of the problem-solving process, including the problem statement, research and analysis results, solution history with iterations, the final solution, critique, recommendation, and the path to the markdown file.


## Testing Your Implementation

After completing the activity tasks, you can test your implementation using:

```bash
python app.py
```

This will present you with an interactive console where you can:
1. Run the demo with a pre-defined problem about employee retention
2. Enter your own problem to solve in interactive mode
3. Exit the application

The application contains a menu system that allows you to easily switch between these options. When you select an option, the system will display the progress of each agent as it works through the problem-solving process and show the final solution in the console.

Note that the application execution time could last three to five minutes, or longer, depending on the problem statement complexity and your hardware environment. Each agent takes time to process its inputs and generate thoughtful outputs.

A detailed markdown report will be saved to the `outputs` directory. To get a better understanding of what to expect, review these example files:

- [Demo Terminal Output](reference_documents/resources/demo.md) - See an example of the complete terminal output during a demo run
- [Sample Problem Solution](reference_documents/resources/problem_solving_20250416_053923.md) - Review a complete problem-solving report from an interactive session
- [Sample Problem Sets](reference_documents/resources/sample_problem_sets.md) - Explore a variety of problem statements across different domains that you can use during testing

When testing your implementation, try using problems from the sample problem sets to verify that your system can handle different types of complex problems effectively.



## Extension Options

Here are some ways to extend this activity after completing the basic implementation:

1. **Add a Memory Component**
   - Implement a shared knowledge repository that stores insights from previous problem-solving sessions
   - Allow agents to query and update the repository
   - Develop a mechanism for transferring learning from one problem to another

2. **Implement Parallel Analysis Agents**
   - Create multiple specialized analysis agents that focus on different aspects of the problem
   - Develop a consensus mechanism to aggregate their findings
   - Implement agent selection based on problem characteristics

3. **Create a Web Interface**
   - Build a simple web interface using Streamlit or Flask
   - Display the step-by-step problem-solving process
   - Allow users to intervene and provide additional guidance at any stage


## Conclusion

This activity focuses on implementing a multi-agent system with LangGraph to solve complex problems through hierarchical decomposition and specialized agents. We'll create a system that intelligently processes problems by breaking them down into research, analysis, solution generation, and critical review phases. This reinforces the principles of multi-agent systems and demonstrates how to implement directed workflows in LangGraph that enable effective collaboration between specialized agents.
