#!/bin/bash

# Export DATABASE_URL for all servers
export DATABASE_URL=postgresql://jgrayson@localhost/holocron
echo "Stopping old servers..."
# Kill specific python processes related to our servers
pkill -f "server.py" || true
sleep 2

echo "Starting Main Server (5005)..."
nohup python3 -u server.py > server.log 2>&1 &
echo $! > server.pid

echo "Starting SkillWeaver (5003)..."
nohup python3 -u templates/skillweaver_server.py > skillweaver.log 2>&1 &
echo $! > skillweaver.pid

echo "Starting GoblinStack (5004)..."
nohup python3 -u templates/goblinstack_server.py > goblinstack.log 2>&1 &
echo $! > goblinstack.pid

echo "Waiting for servers to initialize..."
sleep 3
echo "Current Python Processes:"
ps aux | grep "server.py" | grep -v grep
echo "Servers started!"
