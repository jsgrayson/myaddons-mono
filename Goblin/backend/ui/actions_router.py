from fastapi import APIRouter
import subprocess
import time
import os

router = APIRouter()

# List of valid agent container names
VALID_AGENTS = {
    "warden":       "goblin-warden",
    "tsm_brain":    "goblin-tsm_brain",
    "ah_runner":    "goblin-ah_runner",
    "bank_runner":  "goblin-bank_runner",
    "ml_worker":    "goblin-ml_worker"
}

# Directory holding maintenance scripts inside /opt/goblin
GOBLIN_ROOT = "/opt/goblin"
BACKUP_SCRIPT = f"{GOBLIN_ROOT}/ops/backup/backup_goblin.sh"
UPDATE_SCRIPT = f"{GOBLIN_ROOT}/ops/maintenance/update_goblin.sh"


# --------------------------------------------------------
# Docker Helper
# --------------------------------------------------------
def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except Exception as e:
        return {"error": str(e), "returncode": -1}


# --------------------------------------------------------
# AGENT ACTIONS
# --------------------------------------------------------

@router.post("/ui/actions/start/{agent}")
async def start_agent(agent: str):
    if agent not in VALID_AGENTS:
        return {"status": "error", "message": "Invalid agent"}

    container = VALID_AGENTS[agent]
    result = run_cmd(f"docker compose -f {GOBLIN_ROOT}/docker-compose.yml up -d {container}")
    return {"status": "ok", "action": "start", "agent": agent, "result": result}


@router.post("/ui/actions/stop/{agent}")
async def stop_agent(agent: str):
    if agent not in VALID_AGENTS:
        return {"status": "error", "message": "Invalid agent"}

    container = VALID_AGENTS[agent]
    result = run_cmd(f"docker stop {container}")
    return {"status": "ok", "action": "stop", "agent": agent, "result": result}


@router.post("/ui/actions/restart/{agent}")
async def restart_agent(agent: str):
    if agent not in VALID_AGENTS:
        return {"status": "error", "message": "Invalid agent"}

    container = VALID_AGENTS[agent]
    result = run_cmd(f"docker restart {container}")
    return {"status": "ok", "action": "restart", "agent": agent, "result": result}


# --------------------------------------------------------
# SYSTEM ACTIONS
# --------------------------------------------------------

@router.post("/ui/actions/backup")
async def run_backup():
    if not os.path.exists(BACKUP_SCRIPT):
        return {"status": "error", "message": "Backup script not found"}

    result = run_cmd(f"bash {BACKUP_SCRIPT}")
    return {"status": "ok", "action": "backup", "result": result}


@router.post("/ui/actions/update")
async def run_update():
    if not os.path.exists(UPDATE_SCRIPT):
        return {"status": "error", "message": "Update script not found"}

    result = run_cmd(f"bash {UPDATE_SCRIPT}")
    return {"status": "ok", "action": "update", "result": result}

