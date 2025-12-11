#!/bin/bash
set -e

LOG_ROOT="/opt/goblin/data/logs"

COMPONENT=$1

if [ -z "$COMPONENT" ]; then
    echo "Usage: ./view_logs.sh <component>"
    echo "Available components:"
    echo "  backend"
    echo "  warden"
    echo "  tsm_brain"
    echo "  bank_runner"
    echo "  ah_runner"
    echo "  ml"
    exit 1
fi

LOG_DIR="$LOG_ROOT/$COMPONENT"

if [ ! -d "$LOG_DIR" ]; then
    echo "❌ Log directory not found: $LOG_DIR"
    exit 1
fi

echo "======================================================"
echo "  Viewing logs for: $COMPONENT"
echo "  Location: $LOG_DIR"
echo "======================================================"

LATEST_LOG=$(ls -t $LOG_DIR/*.log 2>/dev/null | head -n 1)

if [ -z "$LATEST_LOG" ]; then
    echo "❌ No log files found for component: $COMPONENT"
    exit 1
fi

echo "➡ Streaming log file: $LATEST_LOG"
echo "======================================================"

tail -n 200 -F "$LATEST_LOG"

