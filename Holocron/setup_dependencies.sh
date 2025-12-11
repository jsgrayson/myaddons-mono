#!/bin/bash
echo "🛠️  Setting up dependencies for all projects..."

# 1. Setup GoblinStack (Python)
echo "--------------------------------"
echo "💰 Setting up GoblinStack..."
cd /Users/jgrayson/Documents/goblin-clean-1
# Install requirements if they exist, otherwise install minimal needs
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
fi
pip3 install fastapi uvicorn jinja2 python-multipart requests

# 2. Setup SkillWeaver (Node.js)
echo "--------------------------------"
echo "⚔️  Setting up SkillWeaver..."
cd /Users/jgrayson/Documents/goblin-clean-1/skillweaver-web
if [ ! -d "node_modules" ]; then
    echo "   Installing Node modules (this may take a minute)..."
    npm install
else
    echo "   Node modules already installed."
fi

echo "--------------------------------"
echo "✅ Setup complete! Now try running ./start_all.sh again."
