#!/bin/bash
set -e

echo "======================================================"
echo "               GOBLIN RESTORE UTILITY                 "
echo "======================================================"

BACKUP_ARCHIVE=$1

if [ -z "$BACKUP_ARCHIVE" ]; then
    echo "Usage: ./restore_goblin.sh <backup_file.tgz>"
    exit 1
fi

if [ ! -f "$BACKUP_ARCHIVE" ]; then
    echo "❌ Backup archive not found: $BACKUP_ARCHIVE"
    exit 1
fi

echo "➡ Stopping Goblin..."
systemctl stop goblin || true

echo "➡ Extracting backup..."
mkdir -p /opt/goblin_restore
tar -xzf "$BACKUP_ARCHIVE" -C /opt/goblin_restore

RESTORE_DIR=$(ls /opt/goblin_restore)

echo "➡ Restoring environment file..."
cp "/opt/goblin_restore/$RESTORE_DIR/.env" /opt/goblin/.env

echo "➡ Restoring data volume..."
rm -rf /opt/goblin/data
cp -r "/opt/goblin_restore/$RESTORE_DIR/data" /opt/goblin/data

echo "➡ Restoring repository source..."
rm -rf /opt/goblin/*
cp -r "/opt/goblin_restore/$RESTORE_DIR/goblin_repo/"* /opt/goblin/

echo "➡ Rebuilding containers..."
cd /opt/goblin
docker compose build

echo "➡ Restarting Goblin..."
systemctl start goblin

echo "======================================================"
echo "    🎉 GOBLIN RESTORED SUCCESSFULLY FROM BACKUP! 🎉    "
echo "======================================================"

