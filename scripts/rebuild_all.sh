#!/bin/bash
set -e

echo "Stopping and removing all Goblin containers..."
docker compose down

echo "Rebuilding all images..."
docker compose build

echo "Starting Goblin..."
docker compose up -d

docker compose ps

