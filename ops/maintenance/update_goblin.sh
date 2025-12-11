#!/bin/bash
set -e

echo "======================================================"
echo "             GOBLIN AUTO-UPDATE SCRIPT                "
echo "======================================================"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")

# Ensure run as root
if [ "$(id -u)" != "0" ]; then
   echo "❌ This script must be run as root"
   exit 1
fi

# Ensure Goblin is installed
if [ ! -d /opt/goblin ]; then
    echo "❌ /opt/goblin not found."
    exit 1
fi

cd /opt/goblin

echo "➡ Stopping Goblin systemd service..."
systemctl stop goblin || true

echo "➡ Creating backup directory..."
mkdir -p /opt/goblin_backups/$DATE

echo "➡ Backing up environment + data..."
cp .env /opt/goblin_backups/$DATE/.
cp -r data /opt/goblin_backups/$DATE/data

echo "➡ Pulling latest Goblin code from GitHub..."
git pull --rebase --autostash

echo "➡ Rebuilding Goblin Docker images..."
docker compose build

echo "➡ Restarting Goblin..."
systemctl start goblin

echo "➡ Checking container status..."
docker compose ps

echo "======================================================"
echo "   🎉 GOBLIN UPDATED SUCCESSFULLY ON $DATE            "
echo "======================================================"

