# ==============================================================================
# Customer Churn & LTV Engine - Production Dockerfile
# Containerizes the FastAPI real-time prediction and LTV inference service
# ==============================================================================

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code, models, and data
COPY src/ src/
COPY models/ models/
COPY data/ data/
COPY dashboard/ dashboard/
COPY sql/ sql/

# Expose API port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI inference service
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
