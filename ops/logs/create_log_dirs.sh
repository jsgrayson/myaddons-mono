#!/bin/bash
set -e

LOG_ROOT="/opt/goblin/data/logs"

echo "======================================================"
echo "         Goblin Log Directory Initialization           "
echo "======================================================"

mkdir -p $LOG_ROOT/backend
mkdir -p $LOG_ROOT/warden
mkdir -p $LOG_ROOT/tsm_brain
mkdir -p $LOG_ROOT/bank_runner
mkdir -p $LOG_ROOT/ah_runner
mkdir -p $LOG_ROOT/ml

echo "➡ Log directories created under: $LOG_ROOT"

echo "======================================================"
echo "           Log directory setup complete.              "
echo "======================================================"

