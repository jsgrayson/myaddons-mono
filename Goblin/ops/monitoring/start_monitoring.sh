#!/bin/bash
set -e

echo "Starting Goblin Monitoring Stack..."
docker compose -f /opt/goblin/docker-compose.yml \
               -f /opt/goblin/ops/monitoring/docker-compose.override.yml up -d

echo "Monitoring is live:"
echo "Prometheus ➜ http://<server_ip>:9090"
echo "cAdvisor   ➜ http://<server_ip>:8080"
echo "Grafana    ➜ http://<server_ip>:3000"

