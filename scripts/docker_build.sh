#!/bin/bash
set -e

echo "Building all Goblin Docker images..."
docker compose build
echo "Build complete."

