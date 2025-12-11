#!/bin/bash

# Holocron Suite Installer
# Sets up the environment for Holocron, SkillWeaver, and PetWeaver.

echo "========================================"
echo "   Holocron Suite Installer"
echo "========================================"

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi
echo "✅ Python 3 found."

# 2. Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client (psql) not found. Database setup might fail."
    echo "   (You can ignore this if using a remote DB)"
else
    echo "✅ PostgreSQL client found."
fi

# 3. Check Docker (Required for SimC)
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found. SimulationCraft integration will be disabled."
    echo "   To enable SimC, install Docker Desktop: https://www.docker.com/products/docker-desktop/"
else
    echo "✅ Docker found."
fi

# 3. Setup Virtual Environment
echo "----------------------------------------"
echo "📦 Setting up Python Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   Created 'venv'."
else
    echo "   'venv' already exists."
fi

# Activate venv
source venv/bin/activate

# 4. Install Dependencies
echo "----------------------------------------"
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found! Installing core packages..."
    pip install flask psycopg2-binary requests networkx python-dotenv
fi

# 5. Database Setup
echo "----------------------------------------"
echo "🗄️  Database Setup"
read -p "Do you want to initialize the database schema? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -z "$DATABASE_URL" ]; then
        echo "   Please enter your Database URL (e.g., postgresql://user:pass@localhost/holocron):"
        read DB_URL
        export DATABASE_URL=$DB_URL
    fi
    
    echo "   Running schema scripts..."
    # Order matters!
    psql $DATABASE_URL -f schema.sql
    psql $DATABASE_URL -f schema_codex.sql
    psql $DATABASE_URL -f schema_fabricator.sql
    psql $DATABASE_URL -f schema_fabricator.sql
    
    # Load Seed Data
    if [ -f "data_recipes.sql" ]; then
        echo "   Loading recipe data..."
        psql $DATABASE_URL -f data_recipes.sql > /dev/null
    fi
    
    # Add other schemas as needed
    echo "✅ Database initialized."
fi

# 6. Environment File
echo "----------------------------------------"
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "DATABASE_URL=postgresql://user:pass@localhost/holocron" > .env
    echo "SIMC_PATH=simc" >> .env
    echo "   Created .env. Please edit it with your actual credentials."
else
    echo "✅ .env file exists."
fi

echo "========================================"
echo "🎉 Installation Complete!"
echo "   Run './start_server.sh' to launch Holocron."
echo "========================================"
