#!/bin/bash
set -e

################################################################################
# Goblin Superproject - MASTER CREATION SCRIPT (CLEAN REBUILD)
# Target: ~/Documents/goblin-clean
# Python required: 3.11+
# NO AUTO-GIT-PUSH (manual push)
################################################################################

BASE_DIR="$HOME/Documents/goblin-clean"
SCRIPTS_DIR="$BASE_DIR/scripts"

echo ""
echo "=============================="
echo "  Goblin Superproject Builder"
echo "=============================="
echo ""

# ------------------------------------------------------------------------------
# Step 1 — Create base directory
# ------------------------------------------------------------------------------

echo "[1/10] Creating base directory at $BASE_DIR ..."
mkdir -p "$BASE_DIR"
mkdir -p "$SCRIPTS_DIR"

# ------------------------------------------------------------------------------
# Step 2 — Ensure Python 3.11+ exists (safe POSIX)
# ------------------------------------------------------------------------------

echo "[2/10] Checking for Python 3.11+ ..."

if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN=$(command -v python3.11)
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=$(command -v python3)
else
    echo "ERROR: Python 3.11+ is required but was not found."
    exit 1
fi

echo "Using Python interpreter: $PYTHON_BIN"

# ------------------------------------------------------------------------------
# Step 3 — Create virtual environment
# ------------------------------------------------------------------------------

echo "[3/10] Creating virtual environment ..."
cd "$BASE_DIR"
$PYTHON_BIN -m venv venv

echo "Activating environment ..."
source venv/bin/activate

echo "Virtual environment ready."

# ------------------------------------------------------------------------------
# Step 4 — Install base dependencies
# ------------------------------------------------------------------------------

echo "[4/10] Installing dependencies ..."

cat > "$BASE_DIR/requirements.txt" << 'EOF'
fastapi
uvicorn[standard]
pydantic
python-dotenv
requests
pandas
numpy
scikit-learn
schedule
loguru
EOF

pip install --upgrade pip
pip install -r requirements.txt

echo "Dependencies installed."

# ------------------------------------------------------------------------------
# Step 5 — Run subsystem scripts
# ------------------------------------------------------------------------------

echo "[5/10] Running subsystem setup scripts ..."

bash "$SCRIPTS_DIR/setup_backend.sh"
bash "$SCRIPTS_DIR/setup_agents.sh"
bash "$SCRIPTS_DIR/setup_ml.sh"
bash "$SCRIPTS_DIR/setup_ops.sh"
bash "$SCRIPTS_DIR/setup_ui.sh"

echo "Subsystems created."

# ------------------------------------------------------------------------------
# Step 6 — Root-level files
# ------------------------------------------------------------------------------

echo "[6/10] Creating root-level config files ..."

cat > "$BASE_DIR/.gitignore" << 'EOF'
venv/
__pycache__/
*.
