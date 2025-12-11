#!/bin/bash

# Holocron Suite - Complete Deployment Script

echo "================================================================"
echo "   HOLOCRON SUITE - COMPLETE DEPLOYMENT"
echo "================================================================"

# Paths
HOLOCRON_DIR="/Users/jgrayson/Documents/holocron"
SKILLWEAVER_DIR="/Users/jgrayson/Documents/skillweaver"
WOW_ADDONS="/Applications/World of Warcraft/_retail_/Interface/AddOns"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "📦 Deploying Addons..."
echo "----------------------------------------"

# Deploy PetWeaver
if [ -d "$HOLOCRON_DIR/PetWeaver" ]; then
    cp -r "$HOLOCRON_DIR/PetWeaver" "$WOW_ADDONS/"
    echo -e "${GREEN}✓${NC} PetWeaver deployed"
else
    echo -e "${YELLOW}⚠${NC} PetWeaver not found"
fi

# Deploy DeepPockets  
if [ -d "$HOLOCRON_DIR/DeepPockets" ]; then
    cp -r "$HOLOCRON_DIR/DeepPockets" "$WOW_ADDONS/"
    echo -e "${GREEN}✓${NC} DeepPockets deployed"
else
    echo -e "${YELLOW}⚠${NC} DeepPockets not found"
fi

# Deploy HolocronViewer
if [ -d "$HOLOCRON_DIR/HolocronViewer" ]; then
    cp -r "$HOLOCRON_DIR/HolocronViewer" "$WOW_ADDONS/"
    echo -e "${GREEN}✓${NC} HolocronViewer deployed"
else
    echo -e "${YELLOW}⚠${NC} HolocronViewer not found"
fi

# Deploy SkillWeaver
if [ -d "$SKILLWEAVER_DIR" ]; then
    cp -r "$SKILLWEAVER_DIR" "$WOW_ADDONS/SkillWeaver"
    echo -e "${GREEN}✓${NC} SkillWeaver deployed"
else
    echo -e "${YELLOW}⚠${NC} SkillWeaver not found"
fi

echo ""
echo "🌐 Starting Web Services..."
echo "----------------------------------------"

# Kill existing processes
pkill -f "server.py" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

# Start backend
cd "$HOLOCRON_DIR"
nohup python3 server.py > server.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > server.pid
echo -e "${GREEN}✓${NC} Backend started (PID: $BACKEND_PID) on http://localhost:5005"

# Wait for backend to start
sleep 2

# Start frontend
cd "$HOLOCRON_DIR/frontend"
nohup npm run dev > dev.log 2>&1 &
echo -e "${GREEN}✓${NC} Frontend starting on http://localhost:3000"

echo ""
echo "📊 Service Status"
echo "----------------------------------------"

sleep 3

# Check if services are running
if lsof -i :5005 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Backend API: running"
else
    echo -e "${YELLOW}⚠${NC} Backend API: not responding"
fi

if lsof -i :3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend: running"
else
    echo -e "${YELLOW}⚠${NC} Frontend: check dev.log"
fi

echo ""
echo "================================================================"
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo "================================================================"
echo ""
echo "🎮 In-Game:"
echo "   1. Launch World of Warcraft"
echo "   2. Type /reload"
echo "   3. Look for minimap buttons for each addon"
echo ""
echo "🌐 Web Dashboard:"
echo "   Open: http://localhost:3000"
echo ""
echo "📝 Logs:"
echo "   Backend: $HOLOCRON_DIR/server.log"
echo "   Frontend: $HOLOCRON_DIR/frontend/dev.log"
echo ""
echo "💾 To sync data after logging in all characters:"
echo "   python3 $HOLOCRON_DIR/sync_addon_data.py"
echo ""
echo "================================================================"
