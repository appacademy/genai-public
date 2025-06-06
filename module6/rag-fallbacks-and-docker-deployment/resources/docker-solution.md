# Docker Solution for High-Availability RAG System

This document contains the Docker configuration files used to containerize the High-Availability RAG system simulation.



## Dockerfile

The Dockerfile defines how to build the container image for the High-Availability RAG system:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY ha_rag_simulation/ ./ha_rag_simulation/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run
CMD ["python", "app.py"]
```

### Dockerfile Explanation

- **Base Image**: Uses `python:3.10-slim` as the base image, which provides a lightweight Python 3.10 environment. Python 3.10 or higher is required to support numpy 2.2.4.
- **Working Directory**: Sets `/app` as the working directory inside the container.
- **Dependencies**: Copies the requirements.txt file and installs the dependencies using pip.
- **Application Code**: Copies the main application file (app.py) and the ha_rag_simulation package into the container.
- **Environment Variables**: Sets `PYTHONUNBUFFERED=1` to ensure Python output isn't buffered, which is important for seeing real-time logs.
- **Command**: Specifies that `python app.py` should be run when the container starts.



## Docker Compose File

The docker-compose.yml file simplifies container management and provides a more declarative way to define the container configuration:

```yaml
version: '3'

services:
  ha-rag-system:
    image: ha-rag-system  # Custom image name for easier reference
    build:
      context: .
      dockerfile: Dockerfile
    stdin_open: true  # equivalent to -i
    tty: true         # equivalent to -t
```

### Docker Compose Explanation

- **Version**: Specifies the Docker Compose file format version.
- **Services**: Defines a service named `ha-rag-system`.
- **Image**: Sets a custom image name (`ha-rag-system`) for easier reference when running Docker commands.
- **Build**: Specifies the build context (current directory) and Dockerfile to use.
- **stdin_open** and **tty**: These options enable interactive mode, which is necessary for the simulation's interactive prompts. They are equivalent to the `-it` flags in the `docker run` command.



## Building and Running

To build and run the containerized application:

```bash
# Build the Docker image using Docker Compose
docker compose build

# Run the container with Docker Compose
docker compose up

# Or run directly with Docker
docker run -it ha-rag-system
```



## Interacting with the Container

The containerized application provides an interactive simulation of a High-Availability RAG system:

- It processes simulated queries through the RAG pipeline
- It demonstrates component failures and fallback mechanisms
- It prompts you to identify circuit breaker states for educational purposes
- You can enter the state (e.g., "closed", "open", "half_open") when prompted
- Use Ctrl+C to stop the container when finished
