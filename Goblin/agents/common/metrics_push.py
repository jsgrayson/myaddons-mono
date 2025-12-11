import requests
import time

BACKEND_PUSH_URL = "http://localhost:8001/status/metrics/push"

def push_metric(agent: str, metric: str, metric_type: str, value: float = 1):
    """
    Push a metric to the Goblin backend aggregator.

    agent: name of the Goblin agent (e.g., 'warden', 'tsm_brain', 'ah_runner')
    metric: name of the metric (e.g., 'jobs_completed', 'errors', 'queue_depth')
    metric_type: "heartbeat", "counter", or "gauge"
    value: numeric value (ignored for heartbeats)
    """

    payload = {
        "agent": agent,
        "metric": metric,
        "type": metric_type,
        "value": value
    }

    try:
        requests.post(BACKEND_PUSH_URL, json=payload, timeout=1)
    except Exception as e:
        # We NEVER want metrics failing to break an agent.
        print(f"[METRICS] Failed to push metric: {agent}/{metric} ({e})")

def push_heartbeat(agent: str):
    """Convenience wrapper for heartbeats."""
    push_metric(agent=agent, metric="heartbeat", metric_type="heartbeat")

def push_counter(agent: str, metric: str, value: float = 1):
    """Convenience wrapper for counters."""
    push_metric(agent=agent, metric=metric, metric_type="counter", value=value)

def push_gauge(agent: str, metric: str, value: float):
    """Convenience wrapper for gauges."""
    push_metric(agent=agent, metric=metric, metric_type="gauge", value=value)
