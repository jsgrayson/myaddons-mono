from fastapi import APIRouter, Request
from prometheus_client import CollectorRegistry, Gauge, Counter, generate_latest
import time

router = APIRouter()

# ------------------------------
# Prometheus Registry
# ------------------------------
registry = CollectorRegistry()

# Core backend metrics
BACKEND_UP = Gauge("goblin_backend_up", "Goblin backend running", registry=registry)
BACKEND_LATENCY = Gauge("goblin_backend_latency_ms", "Backend latency in ms", registry=registry)

# Dynamic storage for agent metrics
AGENT_HEARTBEATS = {}
AGENT_COUNTERS = {}
AGENT_GAUGES = {}

# ------------------------------
# Push endpoint: /status/metrics/push
# ------------------------------
@router.post("/status/metrics/push")
async def push_metrics(request: Request):
    data = await request.json()

    agent = data.get("agent")
    metric = data.get("metric")
    metric_type = data.get("type")
    value = data.get("value", 1)

    if not agent or not metric or not metric_type:
        return {"status": "error", "message": "Missing fields"}

    # ------------------------------
    # Heartbeat = gauge updated with timestamp
    # ------------------------------
    if metric_type == "heartbeat":
        if agent not in AGENT_HEARTBEATS:
            AGENT_HEARTBEATS[agent] = Gauge(
                f"goblin_agent_heartbeat_{agent}",
                f"Heartbeat timestamp for {agent}",
                registry=registry
            )
        AGENT_HEARTBEATS[agent].set(time.time())
        return {"status": "ok"}

    # ------------------------------
    # Counter metrics
    # ------------------------------
    if metric_type == "counter":
        key = f"{agent}_{metric}"
        if key not in AGENT_COUNTERS:
            AGENT_COUNTERS[key] = Counter(
                f"goblin_{key}",
                f"{metric} counter for {agent}",
                registry=registry
            )
        AGENT_COUNTERS[key].inc(value)
        return {"status": "ok"}

    # ------------------------------
    # Gauge metrics
    # ------------------------------
    if metric_type == "gauge":
        key = f"{agent}_{metric}"
        if key not in AGENT_GAUGES:
            AGENT_GAUGES[key] = Gauge(
                f"goblin_{key}",
                f"{metric} gauge for {agent}",
                registry=registry
            )
        AGENT_GAUGES[key].set(value)
        return {"status": "ok"}

    return {"status": "error", "message": "Invalid metric type"}

# ------------------------------
# GET endpoint: /status/metrics (for Prometheus)
# ------------------------------
@router.get("/status/metrics")
async def get_metrics():
    BACKEND_UP.set(1)
    BACKEND_LATENCY.set(5)  # placeholder, can calculate real latency
    return generate_latest(registry)

