#!/bin/bash
set -e

echo "======================================================"
echo "          Goblin systemd Installer / Refresher        "
echo "======================================================"

# Ensure root privileges
if [ "$(id -u)" != "0" ]; then
   echo "❌ This script must be run as root"
   exit 1
fi

# Ensure Goblin directory exists
if [ ! -d /opt/goblin ]; then
    echo "❌ /opt/goblin not found."
    echo "Make sure Goblin is cloned to /opt/goblin before running."
    exit 1
fi

echo "➡ Installing Goblin systemd service..."

cat << 'EOF' > /etc/systemd/system/goblin.service
[Unit]
Description=Goblin Superproject (Docker Compose)
After=network.target docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/goblin
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

echo "➡ Reloading systemd..."
systemctl daemon-reload

echo "➡ Enabling Goblin on boot..."
systemctl enable goblin

echo "➡ Starting Goblin..."
systemctl start goblin

echo "➡ Checking Goblin status..."
systemctl status goblin --no-pager

echo "======================================================"
echo "   🎉 Goblin systemd service installed successfully!   "
echo "======================================================"

