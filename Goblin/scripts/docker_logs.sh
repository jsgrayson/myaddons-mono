#!/bin/bash
set -e

SERVICE=$1

if [ -z "$SERVICE" ]; then
  echo "Usage: ./docker_logs.sh <service-name>"
  echo "Example: ./docker_logs.sh goblin-backend"
  exit 1
fi

docker compose logs -f $SERVICE

