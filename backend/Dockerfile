FROM python:3.11-slim

# Prevent Python stdout buffering
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY ../requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy backend code
COPY . /app

# Expose FastAPI port
EXPOSE 8001

# Healthcheck
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --retries=3 \
    CMD curl -f http://localhost:8001/status/health || exit 1

# Run UVicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
