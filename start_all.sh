#!/bin/bash
# Holocron Unified Startup Script

echo "🚀 Starting Holocron Systems..."

# Set database URL
export DATABASE_URL='postgresql://holocron:password@localhost:5432/holocron_db'

# Start Holocron (main dashboard) on port 5001
echo "📊 Starting Holocron Dashboard (port 5001)..."
cd /Users/jgrayson/Documents/holocron
python3 server.py &
HOLOCRON_PID=$!

# Wait a moment for Holocron to start
sleep 2

# Start PetWeaver on port 5002
echo "🐾 Starting PetWeaver (port 5002)..."
cd /Users/jgrayson/Documents/petweaver
python3 app.py &
PETWEAVER_PID=$!



# 3. Start GoblinStack (FastAPI)
echo "   Starting GoblinStack (Port 5004)..."
cd /Users/jgrayson/Documents/goblin-clean-1
python3 -m uvicorn backend.main:app --port 5004 > /tmp/goblin.log 2>&1 &
GOBLIN_PID=$!
echo "   ✅ GoblinStack started (PID: $GOBLIN_PID)"

# 4. Start SkillWeaver (Python)
echo "   Starting SkillWeaver (Port 3000)..."
cd /Users/jgrayson/Documents/skillweaver-web
python3 app.py > /tmp/skillweaver.log 2>&1 &
SKILL_PID=$!
echo "   ✅ SkillWeaver started (PID: $SKILL_PID)"

echo "----------------------------------------"
echo "� All systems operational!"
echo "   - Holocron:   http://localhost:5001"
echo "   - PetWeaver:  http://localhost:5002"
echo "   - Goblin:     http://localhost:5004"
if [ -n "$SKILL_PID" ]; then
    echo "   - SkillWeaver: http://localhost:3000"
fi
echo "----------------------------------------"
echo "Press Ctrl+C to stop all services."

# Trap Ctrl+C (SIGINT) and kill all background processes
trap "kill $HOLOCRON_PID $PETWEAVER_PID $GOBLIN_PID $SKILL_PID; exit" SIGINT

# Wait for processes
wait
