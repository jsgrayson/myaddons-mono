import time
import traceback
from agents.common.metrics_push import (
    push_heartbeat,
    push_counter,
    push_gauge
)

class AgentMetrics:
    """
    Drop-in metrics helper for Goblin agents.
    Handles:
    - heartbeats
    - job counters
    - error counters
    - gauges (queue depth, latency, etc.)
    """

    def __init__(self, agent_name: str):
        self.agent = agent_name
        self.last_heartbeat = 0
        self.heartbeat_interval = 30  # seconds

    # ---------------------------------------
    # Heartbeat (every 30 seconds by default)
    # ---------------------------------------
    def heartbeat(self):
        now = time.time()
        if now - self.last_heartbeat >= self.heartbeat_interval:
            push_heartbeat(self.agent)
            self.last_heartbeat = now

    # ---------------------------------------
    # Counters
    # ---------------------------------------
    def job_completed(self):
        push_counter(self.agent, "jobs_completed", 1)

    def job_failed(self):
        push_counter(self.agent, "jobs_failed", 1)

    def error(self, err: Exception):
        push_counter(self.agent, "errors", 1)
        print(f"[{self.agent}] ERROR: {err}")
        traceback.print_exc()

    # ---------------------------------------
    # Gauges
    # ---------------------------------------
    def set_queue_depth(self, count: int):
        push_gauge(self.agent, "queue_depth", count)

    def set_latency(self, ms: float):
        push_gauge(self.agent, "latency_ms", ms)

    # ---------------------------------------
    # Wrapper for agent loops
    # ---------------------------------------
    def track_loop(self, before=None, after=None):
        """
        Wrap your agent's main loop like this:

        metrics.track_loop(
            before=lambda: metrics.set_queue_depth(len(queue)),
            after=lambda start_time: metrics.set_latency((time.time() - start_time)*1000)
        )

        """
        start = time.time()

        if before:
            try:
                before()
            except Exception as e:
                self.error(e)

        self.heartbeat()

        if after:
            try:
                after(start)
            except Exception as e:
                self.error(e)

