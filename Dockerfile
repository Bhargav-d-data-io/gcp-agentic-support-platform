FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Cloud Run requires port 8080
EXPOSE 8080

# Set environment variables for Vertex AI
ENV GOOGLE_GENAI_USE_VERTEXAI=TRUE
ENV PORT=8080

# Start the ADK server
CMD ["adk", "run", "support_agent", "--host", "0.0.0.0", "--port", "8080"]
