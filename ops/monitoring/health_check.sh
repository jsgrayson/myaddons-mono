#!/bin/bash
set -e

echo "======================================================"
echo "               GOBLIN HEALTH CHECK TOOL               "
echo "======================================================"

BACKEND_URL="http://localhost:8001/status/health"
LOG_ROOT="/opt/goblin/data/logs"
DISK_WARN=80           # warn at 80% full
DISK_CRIT=90           # critical at 90%
MEM_WARN=80            # warn at 80% used
MEM_CRIT=90            # critical at 90%

# ------------------------------
# Check Docker service
# ------------------------------
echo "➡ Checking Docker daemon..."
if ! systemctl is-active --quiet docker; then
    echo "❌ Docker service is NOT running!"
    exit 1
fi
echo "✔ Docker is active"

# ------------------------------
# Check Docker containers
# ------------------------------
echo "➡ Checking Goblin containers..."
MISSING=$(docker compose -f /opt/goblin/docker-compose.yml ps --services --filter "status=exited")

if [ ! -z "$MISSING" ]; then
    echo "❌ One or more Goblin containers are STOPPED:"
    echo "$MISSING"
    exit 1
fi

echo "✔ All containers are running"

# ------------------------------
# Check backend API
# ------------------------------
echo "➡ Checking backend heartbeat: $BACKEND_URL"
if ! curl -s --fail "$BACKEND_URL" >/dev/null; then
    echo "❌ Backend API is NOT responding!"
    exit 1
fi
echo "✔ Backend is healthy"

# ------------------------------
# Log scanning for critical errors
# ------------------------------
echo "➡ Scanning logs for errors..."
if grep -R "Traceback\|ERROR\|CRITICAL" $LOG_ROOT/* >/dev/null 2>&1; then
    echo "❌ Errors found in Goblin logs!"
    grep -R "Traceback\|ERROR\|CRITICAL" $LOG_ROOT/* | tail -n 20
    exit 1
fi
echo "✔ No critical errors detected in logs"

# ------------------------------
# Disk usage monitoring
# ------------------------------
echo "➡ Checking disk usage..."
DISK_USED=$(df /opt | awk 'NR==2{print $5}' | sed 's/%//')

if [ "$DISK_USED" -ge "$DISK_CRIT" ]; then
    echo "❌ CRITICAL: Disk usage at ${DISK_USED}%"
    exit 1
elif [ "$DISK_USED" -ge "$DISK_WARN" ]; then
    echo "⚠ Warning: Disk usage at ${DISK_USED}%"
else
    echo "✔ Disk usage healthy: ${DISK_USED}%"
fi

# ------------------------------
# Memory usage monitoring
# ------------------------------
echo "➡ Checking memory usage..."
MEM_USED=$(free | awk '/Mem/ {printf("%.0f", $3/$2 * 100)}')

if [ "$MEM_USED" -ge "$MEM_CRIT" ]; then
    echo "❌ CRITICAL: Memory usage at ${MEM_USED}%"
    exit 1
elif [ "$MEM_USED" -ge "$MEM_WARN" ]; then
    echo "⚠ Warning: Memory usage at ${MEM_USED}%"
else
    echo "✔ Memory usage healthy: ${MEM_USED}%"
fi

echo "======================================================"
echo "     🎉 GOBLIN HEALTH CHECK COMPLETED — ALL GOOD!      "
echo "======================================================"
