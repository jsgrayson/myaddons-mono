#!/bin/bash
echo "Stopping old servers..."
pkill -f python3 || true
sleep 2

echo "Starting Main Server (5005)..."
nohup python3 server.py > server.log 2>&1 &

echo "Starting SkillWeaver (5003)..."
nohup python3 templates/skillweaver_server.py > skillweaver.log 2>&1 &

echo "Starting GoblinStack (5004)..."
nohup python3 templates/goblinstack_server.py > goblinstack.log 2>&1 &

echo "Servers started."
