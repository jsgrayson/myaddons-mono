#!/bin/bash
set -e

################################################################################
# Backend Setup Script
# Creates the entire FastAPI backend structure for Goblin
################################################################################

BASE_DIR="$HOME/Documents/goblin-clean/backend"

echo "[Backend] Creating backend directories ..."

mkdir -p "$BASE_DIR/app/routes"
mkdir -p "$BASE_DIR/app/models"
mkdir -p "$BASE_DIR/app/services"
mkdir -p "$BASE_DIR/app/utils"
mkdir -p "$BASE_DIR/tests"

# ------------------------------------------------------------------------------
# main.py
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/app/main.py" << 'EOF'
from fastapi import FastAPI
from .routes import root, status, agents, ml, tasks

app = FastAPI(title="Goblin Backend API", version="0.1.0")

app.include_router(root.router)
app.include_router(status.router)
app.include_router(agents.router)
app.include_router(ml.router)
app.include_router(tasks.router)

EOF

# ------------------------------------------------------------------------------
# config.py
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/app/config.py" << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY: str = os.getenv("API_KEY", "default")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
EOF

# ------------------------------------------------------------------------------
# logging_config.py
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/app/logging_config.py" << 'EOF'
import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)

    return logger
EOF

# ------------------------------------------------------------------------------
# dependencies.py
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/app/dependencies.py" << 'EOF'
from fastapi import Header, HTTPException
from .config import settings

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
EOF

# ------------------------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------------------------

# root.py
cat > "$BASE_DIR/app/routes/root.py" << 'EOF'
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def index():
    return {"message": "Goblin Backend Running"}
EOF

# status.py
cat > "$BASE_DIR/app/routes/status.py" << 'EOF'
from fastapi import APIRouter

router = APIRouter(prefix="/status")

@router.get("/health")
def health():
    return {"status": "ok"}
EOF

# agents.py
cat > "$BASE_DIR/app/routes/agents.py" << 'EOF'
from fastapi import APIRouter

router = APIRouter(prefix="/agents")

@router.get("/")
def agents():
    return {"agents": ["warden", "tsm_brain", "gmail_archiver", "bank_runner", "ah_runner"]}
EOF

# ml.py
cat > "$BASE_DIR/app/routes/ml.py" << 'EOF'
from fastapi import APIRouter

router = APIRouter(prefix="/ml")

@router.get("/predict")
def predict():
    return {"prediction": 123}
EOF

# tasks.py
cat > "$BASE_DIR/app/routes/tasks.py" << 'EOF'
from fastapi import APIRouter

router = APIRouter(prefix="/tasks")

@router.get("/list")
def list_tasks():
    return {"tasks": []}
EOF

# ------------------------------------------------------------------------------
# MODELS
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/app/models/agent_status.py" << 'EOF'
from pydantic import BaseModel

class AgentStatus(BaseModel):
    name: str
    status: str
EOF

cat > "$BASE_DIR/app/models/prediction.py" << 'EOF'
from pydantic import BaseModel

class Prediction(BaseModel):
    value: float
EOF

cat > "$BASE_DIR/app/models/task.py" << 'EOF'
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str
EOF

# ------------------------------------------------------------------------------
# SERVICES
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/app/services/agent_service.py" << 'EOF'
class AgentService:
    def list_agents(self):
        return ["warden", "tsm_brain", "gmail_archiver", "bank_runner", "ah_runner"]
EOF

cat > "$BASE_DIR/app/services/ml_service.py" << 'EOF'
class MLService:
    def predict(self):
        return 123
EOF

cat > "$BASE_DIR/app/services/task_service.py" << 'EOF'
class TaskService:
    def list_tasks(self):
        return []
EOF

# ------------------------------------------------------------------------------
# UTILS
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/app/utils/scheduler.py" << 'EOF'
import schedule
import time

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
EOF

cat > "$BASE_DIR/app/utils/http_client.py" << 'EOF'
import requests

def get(url):
    return requests.get(url).json()
EOF

cat > "$BASE_DIR/app/utils/file_manager.py" << 'EOF'
def save_text(path, text):
    with open(path, "w") as f:
        f.write(text)
EOF

# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/tests/test_root.py" << 'EOF'
def test_root():
    assert True
EOF

cat > "$BASE_DIR/tests/test_agents.py" << 'EOF'
def test_agents():
    assert True
EOF

cat > "$BASE_DIR/tests/test_ml.py" << 'EOF'
def test_ml():
    assert True
EOF

# ------------------------------------------------------------------------------
# Backend README
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/README.md" << 'EOF'
# Goblin Backend (FastAPI)

This folder contains the backend API for Goblin.
EOF

# ------------------------------------------------------------------------------
# run.sh
# ------------------------------------------------------------------------------

cat > "$BASE_DIR/run.sh" << 'EOF'
#!/bin/bash
source ../venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
EOF
chmod +x "$BASE_DIR/run.sh"

echo "[Backend] Backend created successfully."
