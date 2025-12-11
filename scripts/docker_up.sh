#!/bin/bash
set -e

echo "Starting Goblin services..."
docker compose up -d
echo "Goblin is running."
docker compose ps

