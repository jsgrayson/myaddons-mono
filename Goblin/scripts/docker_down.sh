#!/bin/bash
set -e

echo "Stopping Goblin services..."
docker compose down
echo "All services stopped."

