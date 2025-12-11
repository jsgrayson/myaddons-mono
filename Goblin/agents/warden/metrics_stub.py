import time
from agents.common.agent_metrics_template import AgentMetrics

metrics = AgentMetrics("warden")

def run_warden():
    while True:
        try:
            # ---------------------------------------
            # Example metric: queue depth
            # ---------------------------------------
            task_queue_size = 0  # Replace with actual queue length
            metrics.set_queue_depth(task_queue_size)

            # ---------------------------------------
            # MAIN AGENT LOGIC HERE
            # ---------------------------------------
            # warden_logic()
            # YOUR LOGIC GOES HERE

            # Example: one job completed
            # metrics.job_completed()

        except Exception as e:
            metrics.error(e)

        # Track latency + heartbeat
        metrics.track_loop()

        # Adjust sleep as needed
        time.sleep(1)

