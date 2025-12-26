#!/bin/bash
# SkillWeaver Midnight Launch Script - FIX FOR SYNTAX ERRORS
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           SkillWeaver v6.0 (Quartz Engine)                   ║"
echo "║                    NO SUDO REQUIRED                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Hardware: Unlock Arduino for User Account
echo "🔒 Unlocking Serial Ports..."
sudo chmod 666 /dev/cu.usbmodem* 2>/dev/null || echo "   (No Arduino detected)"

# 2. Security: Kill stale processes
pkill -f "python3.*main.py" 2>/dev/null || true

# 3. Engine: Launch AS USER (Preserves Vision)
echo ""
echo "🚀 Launching SkillWeaver Engine..."
echo "   Press '2' to activate rotation"
echo "   Press Ctrl+C to exit"
echo ""
echo "═══════════════════════════════════════════════════════════════"

cd "$SCRIPT_DIR/Brain"
python3 main.py
