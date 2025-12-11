FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Required for numpy/pandas/sklearn builds
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ml /app/ml

CMD ["python", "-c", "print('ML worker ready.')"]

