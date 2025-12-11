#!/bin/bash
set -e

DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="/opt/goblin_backups/$DATE"

echo "======================================================"
echo "              GOBLIN FULL BACKUP UTILITY              "
echo "======================================================"

# Must run as root
if [ "$(id -u)" != "0" ]; then
    echo "❌ This script must be run as root"
    exit 1
fi

echo "➡ Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

cd /opt/goblin

echo "➡ Backing up .env"
cp .env "$BACKUP_DIR/.env"

echo "➡ Backing up Docker data volumes"
cp -r data "$BACKUP_DIR/data"

echo "➡ Backing up repository code"
cp -r /opt/goblin "$BACKUP_DIR/goblin_repo"

echo "➡ Creating tarball..."
cd /opt/goblin_backups
tar -czf "goblin_backup_$DATE.tgz" "$DATE"

echo "➡ Backup archive created:"
echo "/opt/goblin_backups/goblin_backup_$DATE.tgz"

echo "======================================================"
echo "     🎉 GOBLIN BACKUP COMPLETED SUCCESSFULLY! 🎉       "
echo "======================================================"

