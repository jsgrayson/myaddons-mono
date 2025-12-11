#!/bin/bash
# Holocron Unified Shutdown Script

echo "🛑 Stopping all Holocron systems..."

# Function to kill process on a specific port
kill_port() {
    PORT=$1
    NAME=$2
    PID=$(lsof -t -i:$PORT)
    if [ -n "$PID" ]; then
        echo "   Killing $NAME (Port $PORT, PID $PID)..."
        kill -9 $PID
    else
        echo "   $NAME (Port $PORT) is not running."
    fi
}

echo "----------------------------------------"
kill_port 5001 "Holocron Dashboard"
kill_port 5002 "PetWeaver"
kill_port 5004 "GoblinStack"
kill_port 5003 "SkillWeaver"
echo "----------------------------------------"

echo "✅ All systems shut down."
