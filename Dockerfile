FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser
WORKDIR /app

# Install build essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app ./app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Start API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

