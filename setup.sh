#!/bin/bash

echo "🚀 Setting up PetWeaver Desktop App..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

# Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment exists."
fi

# Activate & Install
echo "⬇️  Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
pip install playwright
playwright install chromium

echo "✅ Setup Complete!"
echo ""
echo "To run the app:"
echo "  source venv/bin/activate"
echo "  python3 app.py"
