#!/bin/bash
set -e

echo "======================================================"
echo "     GOBLIN PROXMOX INSTALLER (Full Auto-Setup)       "
echo "======================================================"

# Ensure run as root
if [ "$(id -u)" != "0" ]; then
   echo "❌ This installer must be run as root"
   exit 1
fi

# Update packages
apt update -y
apt upgrade -y

echo "➡ Installing Docker..."
apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git

# Add Docker repo
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" \
  > /etc/apt/sources.list.d/docker.list

apt update -y
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "✔ Docker Installed"

# Create goblin directory
mkdir -p /opt/goblin
cd /opt/goblin

echo "➡ Cloning Goblin repo..."
git clone https://github.com/jsgrayson/goblin-clean.git /opt/goblin

echo "➡ Copying environment template..."
cp .env.sample .env

echo "➡ Building Goblin Docker images..."
docker compose build

echo "➡ Starting Goblin..."
docker compose up -d

echo "➡ Creating systemd service..."
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

systemctl daemon-reload
systemctl enable goblin
systemctl start goblin

echo "➡ Verifying containers..."
docker compose ps

echo "======================================================"
echo "       🎉 GOBLIN IS FULLY INSTALLED ON PROXMOX! 🎉      "
echo "======================================================"

