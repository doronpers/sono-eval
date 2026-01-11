# Sono-Eval Dockerfile - Multi-stage build for optimized image size

# Build stage
FROM python:3.14-slim as builder

LABEL maintainer="Sono-Eval Team"
LABEL description="Explainable Multi-Path Developer Assessment System"

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt pyproject.toml ./

# Install Python dependencies to /install
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage
FROM python:3.14-slim

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY src/ /app/src/
COPY config/ /app/config/
COPY pyproject.toml /app/

# Create non-root user for security
RUN useradd -m -u 1000 sono && \
    mkdir -p /app/data/memory /app/data/tagstudio /app/models/cache && \
    chown -R sono:sono /app

# Switch to non-root user
USER sono

# Install the package
RUN pip install --no-cache-dir -e .

# Expose API port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/sono/.local/bin:${PATH}"

# Enhanced health check with better intervals
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command with optimized settings
CMD ["uvicorn", "sono_eval.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
