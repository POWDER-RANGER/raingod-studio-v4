# RainGod Comfy Studio Docker Image
# Multi-stage build for production

FROM python:3.10-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ backend/
COPY switchboard/ switchboard/
COPY workflows/ workflows/
COPY scripts/ scripts/

# Copy configuration files
COPY .env.example .env

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Environment variables (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV BACKEND_HOST=0.0.0.0
ENV BACKEND_PORT=8000
ENV OLLAMA_BASE_URL=http://host.docker.internal:11434
ENV COMFYUI_BASE_URL=http://host.docker.internal:8188

# Start backend
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
