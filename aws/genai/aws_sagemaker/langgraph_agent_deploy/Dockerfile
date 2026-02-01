FROM python:3.10-slim

WORKDIR /opt/ml/code

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent_graph.py .
COPY app.py .

# Set environment variables
ENV AWS_REGION=us-east-1
ENV PYTHONUNBUFFERED=1
# Set OPENROUTER_API_KEY at runtime or build time
ENV OPENROUTER_API_KEY=your-open-ai-key-here

# Expose port for SageMaker (8080)
EXPOSE 8080

# Start the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
