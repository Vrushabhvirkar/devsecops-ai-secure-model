# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser
WORKDIR /app

# Minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

USER appuser

ENV HOST=0.0.0.0 PORT=8080
EXPOSE 8080

# MODEL_PATH and MODEL_API_KEY must be provided at runtime
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

