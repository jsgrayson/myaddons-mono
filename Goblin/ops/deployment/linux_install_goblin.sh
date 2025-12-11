#!/bin/bash
set -e

echo "======================================================"
echo "       GOBLIN LINUX INSTALLER (Full Auto-Setup)       "
echo "======================================================"

# Ensure running as root
if [ "$(id -u)" != "0" ]; then
   echo "❌ This installer must be run as root"
   exit 1
fi

echo "➡ Updating system..."
apt update -y
apt upgrade -y

echo "➡ Installing dependencies..."
apt install -y \
    ca-certificates \
    curl \
    gnupg \
    git \
    lsb-release

echo "➡ Adding Docker repository..."
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
  $(lsb_release -cs) stable" \
  > /etc/apt/sources.list.d/docker.list

apt update -y

echo "➡ Installing Docker engine..."
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "✔ Docker installed successfully"

echo "➡ Creating Goblin directory..."
mkdir -p /opt/goblin
cd /opt/goblin

echo "➡ Cloning Goblin repo..."
git clone https://github.com/jsgrayson/goblin-clean.git /opt/goblin

echo "➡ Creating environment file..."
cp .env.sample .env

echo "➡ Building Goblin containers..."
docker compose build

echo "➡ Starting Goblin stack..."
docker compose up -d

echo "➡ Installing systemd service..."
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

echo "➡ Enabling Goblin autostart..."
systemctl daemon-reload
systemctl enable goblin
systemctl start goblin

echo "➡ Verifying containers..."
docker compose ps

echo "======================================================"
echo "   🎉 GOBLIN INSTALLED SUCCESSFULLY ON LINUX SERVER! 🎉  "
echo "======================================================"

