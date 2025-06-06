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
