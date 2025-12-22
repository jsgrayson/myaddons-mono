FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# (libpq-dev is often needed for psycopg2, git for some pip installs)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Default command is handled by docker-compose
CMD ["python", "backend/main.py"]
