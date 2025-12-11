#!/bin/bash
set -e

LOG_ROOT="/opt/goblin/data/logs"

echo "======================================================"
echo "              Goblin Log Cleanup Script               "
echo "======================================================"

echo "➡ Cleaning logs older than 7 days in: $LOG_ROOT"

find $LOG_ROOT -type f -name "*.log.*.gz" -mtime +7 -print -delete
find $LOG_ROOT -type f -name "*.log" -mtime +7 -print -delete

echo "➡ Removing empty log directories (if any)..."
find $LOG_ROOT -type d -empty -print -delete

echo "======================================================"
echo "        🎉 Goblin log cleanup completed!              "
echo "======================================================"

