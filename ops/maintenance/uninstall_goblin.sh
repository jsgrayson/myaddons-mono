#!/bin/bash
set -e

echo "======================================================"
echo "               GOBLIN SAFE UNINSTALLER                "
echo "======================================================"

# Must run as root
if [ "$(id -u)" != "0" ]; then
    echo "❌ This script must be run as root"
    exit 1
fi

echo "➡ Stopping Goblin systemd service (ignore errors)..."
systemctl stop goblin || true

echo "➡ Disabling Goblin autostart..."
systemctl disable goblin || true

echo "➡ Removing Goblin systemd service file..."
rm -f /etc/systemd/system/goblin.service
systemctl daemon-reload

echo "➡ Bringing down Goblin Docker stack..."
if [ -d /opt/goblin ]; then
    cd /opt/goblin
    docker compose down || true
fi

echo "➡ Removing Goblin Docker containers..."
docker rm -f $(docker ps -aq --filter "name=goblin") 2>/dev/null || true

echo "➡ Removing Goblin Docker images..."
docker rmi $(docker images -q --filter "reference=goblin-*") 2>/dev/null || true

echo "➡ Removing Goblin data directories..."
rm -rf /opt/goblin/data
rm -rf /opt/goblin/logs

echo "➡ Removing Goblin source directory..."
rm -rf /opt/goblin

echo "======================================================"
echo "        🎉 GOBLIN HAS BEEN UNINSTALLED CLEANLY!       "
echo "======================================================"
echo "Docker engine remains installed. To remove Docker too:"
echo "    sudo apt purge docker-ce docker-ce-cli     "
echo "    sudo rm -rf /var/lib/docker /var/lib/containerd"
echo "======================================================"

