#!/bin/bash
set -e

################################################################################
# Ops Setup Script (SAFE VERSION)
################################################################################

BASE_DIR="$HOME/Documents/goblin-clean/ops"

echo "[OPS] Creating ops directories ..."

mkdir -p "$BASE_DIR/vm_setup"
mkdir -p "$BASE_DIR/deployment"
mkdir -p "$BASE_DIR/backup"
mkdir -p "$BASE_DIR/monitoring"

################################################################################
# Helper write function
################################################################################

write_file() {
    FILE="$1"
    shift
    printf "%s\n" "$@" > "$FILE"
}

################################################################################
# VM SETUP SCRIPTS
################################################################################

# Proxmox setup
write_file "$BASE_DIR/vm_setup/setup_proxmox.sh" \
"#!/bin/bash" \
"echo 'Configuring Proxmox VM for Goblin...'" \
"apt update && apt install -y python3 python3-venv git" \
"echo 'Proxmox VM setup complete.'"

chmod +x "$BASE_DIR/vm_setup/setup_proxmox.sh"

# macOS setup
write_file "$BASE_DIR/vm_setup/setup_mac.sh" \
"#!/bin/bash" \
"echo 'Running macOS setup for Goblin...'" \
"brew update" \
"brew install python git" \
"echo 'macOS environment ready.'"

chmod +x "$BASE_DIR/vm_setup/setup_mac.sh"

# Ubuntu VM setup
write_file "$BASE_DIR/vm_setup/setup_vm_ubuntu.sh" \
"#!/bin/bash" \
"echo 'Setting up Ubuntu VM for Goblin...'" \
"sudo apt update" \
"sudo apt install -y python3 python3-venv git" \
"echo 'Ubuntu VM configured.'"

chmod +x "$BASE_DIR/vm_setup/setup_vm_ubuntu.sh"

################################################################################
# DEPLOYMENT SCRIPTS
################################################################################

write_file "$BASE_DIR/deployment/deploy_local.sh" \
"#!/bin/bash" \
"echo 'Deploying Goblin locally...'" \
"cd ~/Documents/goblin-clean/backend" \
"source ../venv/bin/activate" \
"uvicorn app.main:app --host 0.0.0.0 --port 8001"

chmod +x "$BASE_DIR/deployment/deploy_local.sh"

write_file "$BASE_DIR/deployment/deploy_remote.sh" \
"#!/bin/bash" \
"echo 'Deploying Goblin on remote server...'" \
"ssh user@server 'cd goblin-clean && bash ops/deployment/deploy_local.sh'"

chmod +x "$BASE_DIR/deployment/deploy_remote.sh"

################################################################################
# BACKUP SCRIPTS
################################################################################

write_file "$BASE_DIR/backup/create_backup.sh" \
"#!/bin/bash" \
"echo 'Creating Goblin backup...'" \
"tar -czf goblin-backup-$(date +%Y%m%d).tar.gz ~/Documents/goblin-clean"

chmod +x "$BASE_DIR/backup/create_backup.sh"

write_file "$BASE_DIR/backup/restore_backup.sh" \
"#!/bin/bash" \
"echo 'Restoring Goblin backup...'" \
"tar -xzf \$1 -C ~/Documents/"

chmod +x "$BASE_DIR/backup/restore_backup.sh"

################################################################################
# MONITORING SCRIPTS
################################################################################

write_file "$BASE_DIR/monitoring/check_services.sh" \
"#!/bin/bash" \
"echo 'Checking Goblin services...'" \
"pgrep -f uvicorn && echo 'Backend: OK' || echo 'Backend: DOWN'"

chmod +x "$BASE_DIR/monitoring/check_services.sh"

write_file "$BASE_DIR/monitoring/health_report.sh" \
"#!/bin/bash" \
"echo 'Generating Goblin health report...'" \
"echo 'Disk usage:'" \
"df -h | grep Users" \
"echo ''" \
"echo 'Top processes:'" \
"ps aux | head"

chmod +x "$BASE_DIR/monitoring/health_report.sh"

################################################################################
# Done
################################################################################

echo "[OPS] Ops subsystem created successfully."
