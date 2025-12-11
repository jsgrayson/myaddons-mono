#!/bin/bash
set -e

echo "======================================================"
echo "    GOBLIN RASPBERRY PI INSTALLER (ARM64 Auto-Setup)  "
echo "======================================================"

# Ensure running as root
if [ "$(id -u)" != "0" ]; then
   echo "❌ This installer must be run as root"
   exit 1
fi

echo "➡ Updating system..."
apt update -y
apt upgrade -y

echo "➡ Installing Docker dependencies..."
apt install -y \
    ca-certificates \
    curl \
    gnupg \
    git \
    lsb-release

echo "➡ Installing Docker (ARM64)..."

# Set up Docker repo
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

apt install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-compose-plugin

echo "✔ Docker installed on Raspberry Pi"

# Create Goblin directory
mkdir -p /opt/goblin
cd /opt/goblin

echo "➡ Cloning Goblin repo from GitHub..."
git clone https://github.com/jsgrayson/goblin-clean.git /opt/goblin

echo "➡ Creating environment file..."
cp .env.sample .env

echo "➡ Building Docker containers..."
docker compose build

echo "➡ Starting Goblin stack..."
docker compose up -d

echo "➡ Installing systemd service..."
cat << 'EOF' > /etc/system

