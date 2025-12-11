#!/bin/bash
set -e

echo "======================================================"
echo "             GOBLIN DISASTER RECOVERY TOOL            "
echo "======================================================"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")

BACKUP_ARCHIVE=$1

if [ -z "$BACKUP_ARCHIVE" ]; then
    echo "Usage: ./disaster_recovery.sh <backup_file.tgz>"
    exit 1
fi

if [ ! -f "$BACKUP_ARCHIVE" ]; then
    echo "❌ Backup archive not found: $BACKUP_ARCHIVE"
    exit 1
fi

echo "➡ Starting full system recovery..."

echo "➡ Updating and installing dependencies..."
apt update -y
apt install -y ca-certificates curl gnupg git lsb-release

echo "➡ Installing Docker..."
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg \
    | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
  $(lsb_release -cs) stable" \
  > /etc/apt/sources.list.d/docker.list

apt update -y
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "✔ Docker installed"

echo "➡ Creating Goblin directory..."
mkdir -p /opt/goblin_restore
tar -xzf "$BACKUP_ARCHIVE" -C /opt/goblin_restore

RESTORE_DIR=$(ls /opt/goblin_restore)

echo "➡ Extracted backup to /opt/goblin_restore/$RESTORE_DIR"

echo "➡ Cloning fresh Goblin codebase..."
git clone https://github.com/jsgrayson/goblin-clean.git /opt/goblin

echo "➡ Restoring environment..."
cp "/opt/goblin_restore/$RESTORE_DIR/.env" /opt/goblin/.env

echo "➡ Restoring data volume..."
rm -rf /opt/goblin/data
cp -r "/opt/goblin_restore/$RESTORE_DIR/data" /opt/goblin/data

echo "➡ Rebuilding Goblin containers..."
cd /opt/goblin
docker compose build

echo "➡ Starting Goblin containers..."
docker compose up -d

echo "➡ Reinstalling systemd service..."
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

echo "➡ Checking containers..."
docker compose ps

echo "======================================================"
echo "   🎉 FULL GOBLIN RECOVERY COMPLETED SUCCESSFULLY!     "
echo "======================================================"

