#!/bin/bash

# CONFIG
HOST="r720-goblin-server"
USER="goblin"
REPO_URL="https://github.com/jgrayson/goblin-core.git" # Placeholder
DEST_DIR="/opt/goblin-core"

echo "[GOBLIN] Initiating Deployment Sequence to $HOST..."

# 1. SSH & CLONE
ssh $USER@$HOST << EOF
    # Setup Directory
    if [ ! -d "$DEST_DIR" ]; then
        echo "[REMOTE] Cloning Repo..."
        git clone $REPO_URL $DEST_DIR
    else
        echo "[REMOTE] Pulling Updates..."
        cd $DEST_DIR && git pull
    fi

    # 2. MOUNT NETWORK SHARES (WoW WTF)
    # Ensure /mnt/wow_share exists. This assumes you have setup the SMB mount in /etc/fstab on the R720 already.
    if mountpoint -q /mnt/wow_share; then
        echo "[REMOTE] WoW Share Mounted."
    else
        echo "[REMOTE] WARNING: WoW Share NOT Mounted at /mnt/wow_share."
    fi

    # 3. DOCKER DEPLOY
    echo "[REMOTE] Spinning up Microservices..."
    cd $DEST_DIR
    docker-compose up -d --build

    # 4. HEALTH CHECK
    echo "[REMOTE] Verifying Services..."
    docker ps | grep goblin
EOF

echo "[GOBLIN] Deployment Complete. Dashboard available at http://$HOST:8000"
