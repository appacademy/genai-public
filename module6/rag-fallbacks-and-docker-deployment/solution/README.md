# High-Availability RAG System and Deployment Preparation

## Overview

This project implements a simulation of a High-Availability Retrieval-Augmented Generation (RAG) system that demonstrates resilience patterns for production AI applications. The system is designed to gracefully degrade rather than completely fail when faced with service disruptions, implementing circuit breaker patterns and multi-tiered fallbacks for different RAG components.

### Key Features

- **Circuit Breaker Pattern**: Monitors component health and prevents cascading failures
- **Multi-Tier Fallback Strategies**: Graceful degradation pathways for each component
- **Component Health Monitoring**: Tracks failure rates and response times
- **Interactive Testing**: Simulates failures and demonstrates resilience mechanisms
- **Docker Containerization**: Enables consistent deployment across environments

## Prerequisites

- **Python 3.10+** (required for numpy 2.2.4 compatibility)
- **Docker** (optional, for containerization)

## Setup Instructions

### Local Setup

1. Clone the repository (if you haven't already)

2. Create and activate a virtual environment:

   **Windows (PowerShell)**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

   **Mac/Linux**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Copy the template file
   cp .env.template .env
   
   # Optionally edit the .env file to customize the OLLAMA_API_URL
   # Default is: OLLAMA_API_URL="http://localhost:11434"
   ```

## Running the Application

### Running Locally

To run the simulation locally:

```bash
python app.py
```

This will start the interactive simulation that demonstrates the High-Availability RAG system's resilience patterns. The simulation will:

1. Process a series of queries through the RAG pipeline
2. Simulate component failures based on configured failure rates
3. Demonstrate fallback mechanisms when components fail
4. Display system health metrics and circuit breaker states
5. Prompt you to identify circuit breaker states for educational purposes

### Running with Docker

#### Building and Running with Docker Compose

```bash
# Build the Docker image
docker compose build

# Run the container
docker compose up
```

#### Running with Docker directly

```bash
# Build the image (if not using docker compose)
docker build -t ha-rag-system .

# Run the container
docker run -it ha-rag-system
```

#### Interacting with the Container

The containerized application provides the same interactive experience as the local version:

- It processes simulated queries through the RAG pipeline
- It demonstrates component failures and fallback mechanisms
- It prompts you to identify circuit breaker states
- Enter the state (e.g., "closed", "open", "half_open") when prompted
- Use Ctrl+C to stop the container when finished

## Project Structure

The project follows a modular architecture that separates core framework components from specific implementations:

```
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

### Key Components

- **Embedders**: Convert text into vector embeddings (primary, secondary, cached)
- **Retrievers**: Find relevant documents using embeddings (primary, reduced, none)
- **Generators**: Create responses using retrieved context (primary, fallback, template)
- **Circuit Breakers**: Monitor component health and manage state transitions
- **Fallback Strategies**: Define degradation pathways when components fail

## Documentation

For more detailed information, refer to the following documentation:

- **Activity Instructions**: `reference_docs/activity-deployment-preperation-with-docker-containers.md`
- **Docker Solution**: `reference_docs/_assets/docker-solution.md`
- **Resilience Patterns**: `reference_docs/_assets/rag-resilience-patterns-explained.md`
- **Test Scenarios**: `reference_docs/_assets/rag-test-scenarios-analysis.md`
