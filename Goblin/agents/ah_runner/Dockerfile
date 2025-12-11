FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY ../../requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["python", "ah_runner.py"]

