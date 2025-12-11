from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import psutil
import docker
import time

router = APIRouter()

# Use the new templates directory with premium dashboards
templates = Jinja2Templates(directory="backend/templates")
try:
    docker_client = docker.from_env()
except Exception:
    docker_client = None

# Mount static files for CSS/JS
from fastapi import FastAPI
static_app = FastAPI()
static_app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@router.get("/ui", response_class=HTMLResponse)
async def ui_dashboard(request: Request):
    # ------------------------------
    # System Metrics
    # ------------------------------
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    # ------------------------------
    # Docker Container Status
    # ------------------------------
    containers = []
    if docker_client:
        try:
            containers_list = docker_client.containers.list(all=True)
            for c in containers_list:
                containers.append({
                    "name": c.name,
                    "status": c.status,
                    "id": c.short_id
                })
        except Exception:
            pass

    # ------------------------------
    # Agent Heartbeats
    # (from Prometheus / backend metrics system)
    # ------------------------------
    # This is placeholder — Phase 2 will read real metrics.
    agent_status = {
        "warden": "unknown",
        "tsm_brain": "unknown",
        "ah_runner": "unknown",
        "bank_runner": "unknown",
        "ml_worker": "unknown"
    }

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "cpu": cpu,
        "mem": mem,
        "disk": disk,
        "containers": container_status,
        "agent_status": agent_status,
        "timestamp": int(time.time())
    })

# Premium WoW-themed dashboards
@router.get("/", response_class=HTMLResponse)
async def goblin_dashboard(request: Request):
    return templates.TemplateResponse("goblinstack_dashboard.html", {"request": request})

@router.get("/markets", response_class=HTMLResponse)
async def markets(request: Request):
    return templates.TemplateResponse("goblinstack_markets.html", {"request": request})

@router.get("/predictions", response_class=HTMLResponse)
async def predictions(request: Request):
    return templates.TemplateResponse("goblinstack_predictions.html", {"request": request})

@router.get("/alerts", response_class=HTMLResponse)
async def alerts(request: Request):
    return templates.TemplateResponse("goblinstack_alerts.html", {"request": request})

@router.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    return templates.TemplateResponse("goblinstack_settings.html", {"request": request})

# API endpoints for dashboard data
@router.get("/api/market-data")
async def get_market_data():
    return {
        "items": [
            {"name": "Eternal Crystal", "price": 850, "change": -15.2, "volume": 1250},
            {"name": "Elethium Ore", "price": 425, "change": 8.5, "volume": 3400},
            {"name": "Shadowghast Ingot", "price": 1200, "change": -2.1, "volume": 890}
        ]
    }
