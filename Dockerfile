# Sono-Eval Dockerfile

FROM python:3.11-slim

LABEL maintainer="Sono-Eval Team"
LABEL description="Explainable Multi-Path Developer Assessment System"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/src/
COPY config/ /app/config/

# Create data directories
RUN mkdir -p /app/data/memory /app/data/tagstudio /app/models/cache

# Install the package
RUN pip install -e .

# Expose API port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["uvicorn", "sono_eval.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
