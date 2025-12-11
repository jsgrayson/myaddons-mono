import time
from agents.common.agent_metrics_template import AgentMetrics

metrics = AgentMetrics("bank_runner")

def run_bank_runner():
    while True:
        try:
            # Example: queue depth
            transfer_queue = []
            metrics.set_queue_depth(len(transfer_queue))

            # MAIN LOGIC
            # bank_operations()
            # YOUR LOGIC GOES HERE

            # Example:
            # metrics.job_completed()

        except Exception as e:
            metrics.error(e)

        metrics.track_loop()
        time.sleep(1)

