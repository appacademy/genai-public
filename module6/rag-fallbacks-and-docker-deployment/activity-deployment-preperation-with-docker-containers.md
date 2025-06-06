# High-Availability RAG System and Deployment Preparation

## Overview

In this hands-on activity, you'll build a `HighAvailabilityRAG` class that implements multiple fallback strategies to ensure system reliability even when components fail. You'll create a system that can gracefully degrade rather than completely fail when faced with service disruptions, implementing the circuit breaker pattern and multi-tiered fallbacks for different RAG components.



## Learning Objectives

- Design a `HighAvailabilityRAG` class with well-defined interfaces for embedding, retrieval, and generation components.
- Implement circuit breaker patterns to detect component failures and trigger appropriate fallback mechanisms.
- Develop multi-tier fallback strategies that gracefully degrade service quality rather than failing completely.
- Create a monitoring approach to track component health and performance metrics.
- Configure Docker containers to enable consistent deployment of the high-availability system.



## Time Estimate

60 minutes



## Prerequisites

-   Python 3.12 (as used in the project setup)



## Setup Instructions



1. ### Step 1: Clone the Repository

   Clone the starter code repository to your local machine:

   ```bash
   git clone https://github.com/[organization]/langchain-rag-pipeline.git
   cd langchain-rag-pipeline
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
   cd starter_code
   pip install -r requirements.txt
   ```

   The requirements.txt file contains the following dependencies:

   ```
   numpy==2.2.4
   ```





## Activity Tasks



### Task 1: Setup and Component Design (30 minutes)

1. **Required Reading**: Review the `resources/rag-resilience-patterns-explained.md` document to understand the architecture and resilience patterns used in the system.

2. Examine the three core component types that form the foundation of our RAG system:
   - **Embedders**: Convert text to vector representations.
   - **Retrievers**: Find relevant documents using embeddings.
   - **Generators**: Create text responses using queries and context.

3. Complete the **PrimaryEmbedder** implementation in `components/embedders.py`:
   - Generate a normalized embedding vector using numpy.
   - Study how the SecondaryEmbedder and CachedEmbedder are implemented for reference.
   - Ensure the embedding is properly normalized (unit vector) for consistent similarity calculations.

4. Implement document limiting in the **ReducedRetriever** in `components/retrievers.py`:
   - Modify the max_docs calculation to limit results to at most min(top_k, 2).
   - This simulates a degraded retrieval service that returns fewer documents.

5. Complete the **FallbackGenerator** in `components/generators.py`:
   - Create simplified response text for both cases (with and without context).
   - Ensure the response is more basic than the PrimaryGenerator but still functional.
   - Study how the response format differs from the PrimaryGenerator.



### Task 2: Circuit Breaker Implementation (30 minutes)

1. Understand the Circuit Breaker pattern in `core/circuit_breaker.py`:
   - Study the three circuit states: CLOSED (normal), OPEN (failing), and HALF_OPEN (testing recovery).
   - Examine how the CircuitBreaker monitors component health via the ComponentStatus class.
   - Identify how failures are tracked and how they influence circuit state transitions.

2. Implement the **recovery timeout check** in the execute method:
   - Replace the placeholder condition to check if enough time has passed since the circuit opened.
   - Use the recovery_timeout property and last_state_change_time to determine if a recovery attempt should be made.
   - When the timeout has elapsed, transition the circuit from OPEN to HALF_OPEN state.

3. Implement the **circuit opening logic** in the exception handling section:
   - Replace the placeholder condition to detect when a circuit should open.
   - Check if:
     - There are sufficient samples (total_calls >= min_samples).
     - The failure rate exceeds the threshold (status.get_failure_rate() >= failure_threshold) .
     - The current state is CLOSED.
   - If all conditions are met, transition to the OPEN state.

4. Test the circuit breaker behavior by executing the application and observing how:
   - Circuits open after consecutive failures.
   - Recovery is attempted after the timeout period.
   - Circuits return to the CLOSED state if recovery succeeds.



### Task 3: Fallback Strategy Development (30 minutes)

1. Examine the fallback chain architecture in `core/strategy.py`:
   - Understand how the FallbackStrategy class organizes fallback options.
   - Study the relationship between ComponentType enums and component instances.

2. Complete the **FallbackStrategy initialization** in `core/strategy.py`:
   - Initialize the fallback_chains dictionary with ComponentType keys.
   - Map each component type to its corresponding list of implementations.
   - Use ComponentType.EMBEDDER, ComponentType.RETRIEVER, and ComponentType.GENERATOR as keys.
   - Assign the constructor parameters (embedders, retrievers, generators) as values.

3. Implement the **final fallback mechanism** in the `get_embedding` method in `system.py`:
   - Complete the empty fallback return statement in try_fallback_embedder.
   - Create a zero vector with the same dimension as the primary embedder.
   - Use embedders[0].dimension to determine the correct size.

4. Complete the **RAG pipeline** in the query method in `system.py`:
   - Implement Step 1: Call self.get_embedding with the user_query.
   - Implement Step 2: Call self.get_relevant_documents with the embedding and top_k=3.
   - Implement Step 3: Call self.generate_response with the query and retrieved documents.
   - Return the generated response to the user.

5. Test the complete fallback strategy by executing the application and observing:
   - How primary services fail and trigger fallbacks.
   - The degradation in quality as fallbacks are used.
   - The system's ability to continue functioning despite multiple failures.



### Task 4: Integration and Testing (20 minutes)

1. **Required Reading**: Review the `resources/rag-test-scenarios-analysis.md` document to understand the expected behavior and analysis of different failure scenarios.
2. Connect all components in the `HighAvailabilityRAG` class.
3. Run the `test_high_availability_rag()` function (e.g., by executing `python app.py`).
4. Observe the interactive output: Press Enter after each query to see the system's response, which components failed (if any), which fallbacks were used, and the updated health status/circuit breaker state.
5. Analyze how the system degrades gracefully under simulated failures compared to a complete outage.
6. Review the `get_system_health()` output after each step to track component status changes.



### Task 5: Containerization with Docker (10 minutes)

1. Review the Docker configuration approach for the high-availability RAG system. The complete Docker solution files are available in the `resources/docker-solution.md` document.

2. Understand how the Docker container is configured to run the high-availability RAG system. The solution uses a Dockerfile that specifies a Python 3.10-slim base image (required for numpy 2.2.4 compatibility), sets up a working directory, installs dependencies from requirements.txt, copies the application code, configures environment variables, and specifies the command to run the application.

3. Learn about Docker Compose as a tool for simplifying container management. The solution includes a docker-compose.yml file that defines a service with a custom image name for easier reference and enables interactive mode for the simulation's prompts.

4. **Building and Running the Container**: The containerized application can be built using `docker compose build` and run with either `docker compose up` or `docker run -it ha-rag-system`. The container provides an interactive simulation that demonstrates the high-availability RAG system's resilience patterns.

5. **Interacting with the Container**: When running, the container processes simulated queries, demonstrates component failures and fallback mechanisms, and prompts you to identify circuit breaker states. You can respond to these prompts and observe how the system handles different failure scenarios.

6. **Discussion Points**:
   - **Benefits of containerization for a production RAG system**:
     - Consistency across development and production environments
     - Isolation of dependencies and system requirements
     - Portability across different infrastructure
     - Simplified deployment and scaling
     - Version control for the entire application stack
     - Resource management and monitoring capabilities

   - **Challenges with containerizing components with different resource requirements**:
     - Embedding models may require more memory or GPU resources
     - Retrieval systems might need access to large vector databases
     - LLM generators have varying compute requirements
     - Solutions include: microservices architecture, container orchestration (Kubernetes), 
       resource-aware fallback strategies, and separate containers for resource-intensive components

For more information on Docker containerization, refer to the [official Docker documentation](https://docs.docker.com/get-started/) and the detailed Docker solution in `resources/docker-solution.md`.






## Project Structure

The project follows a modular architecture that separates core framework components from specific implementations:

```plaintext
ha_rag_simulation/
├── __init__.py
├── system.py              # Main HighAvailabilityRAG class
├── test_runner.py         # Testing functions
├── components/            # Component implementations
│   ├── __init__.py
│   ├── embedders.py       # Embedder implementations
│   ├── generators.py      # Generator implementations
│   └── retrievers.py      # Retriever implementations
└── core/                  # Core framework components
    ├── __init__.py
    ├── circuit_breaker.py # Circuit breaker pattern
    ├── enums.py           # Shared enums
    ├── interfaces.py      # Abstract base classes
    ├── status.py          # Component status tracking
    └── strategy.py        # Fallback strategy
```

This structure follows good software engineering practices:
- **Separation of Concerns**: Core framework components are separated from specific implementations
- **Interface-Based Design**: Abstract base classes define clear contracts for components
- **Modularity**: Related functionality is grouped together
- **Extensibility**: New component implementations can be added without modifying the core framework



## Starter Code and Solution Code

-   **Starter Code:** Use the `starter` directory from the main project repository. It contains skeleton classes with `TODO` comments indicating where you need to implement functionality.
-   **Solution Code:** The main project directory contains the completed solution with a fully implemented high-availability RAG system.
-   **Reference Documentation:** 
    - `resources/rag-resilience-patterns-explained.md`: Technical overview of the resilience patterns
    - `resources/rag-test-scenarios-analysis.md`: Analysis of test scenarios and expected behavior



## Extension Options

1. **Quality-Aware Fallback Selection**
   - Enhance the fallback strategy to consider both availability and quality metrics.
   - Implement A/B testing between different component implementations.
   - Add telemetry to track degradation impact on user satisfaction.

2. **Distributed Circuit Breaking**
   - Implement a shared circuit breaker state using Redis or similar.
   - Allow multiple instances to contribute to and respond to the same circuit state.
   - Add alerting when circuits open or remain open for extended periods.

3. **Container Health Monitoring**
   - Add HEALTHCHECK instruction in the Dockerfile
   - Expose a /health endpoint in the application
   - Monitor circuit breaker states as health indicators
   - Configure liveness and readiness probes if using Kubernetes
   - Log health metrics to external monitoring systems



## Conclusion

In this activity, you've built a high-availability RAG system that demonstrates important resilience patterns for production AI applications. By implementing circuit breakers and multi-tier fallback strategies, you've created a system that can gracefully degrade under failure conditions rather than experiencing complete outages.

The skills you've learned—designing with interfaces, implementing resilience patterns, monitoring component health, and containerizing applications—are directly applicable to real-world AI systems. As LLM-powered applications become more prevalent in production environments, the ability to build systems that remain operational even when components fail becomes increasingly valuable.

Remember that in production environments, the principles demonstrated here would be applied to actual embedding services, vector databases, and LLM APIs—each with their own failure modes and performance characteristics. The simulation you've built provides a safe environment to experiment with these patterns before applying them to systems with real dependencies and costs.
