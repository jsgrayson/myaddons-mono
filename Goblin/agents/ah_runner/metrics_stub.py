import time
from agents.common.agent_metrics_template import AgentMetrics

metrics = AgentMetrics("ah_runner")

def run_ah_runner():
    while True:
        try:
            # Example: number of AH scans queued
            scan_queue_size = 0  # Replace with real queue
            metrics.set_queue_depth(scan_queue_size)

            # MAIN LOGIC
            # run_auction_house_logic()
            # YOUR LOGIC HERE

            # Example:
            # metrics.job_completed()

        except Exception as e:
            metrics.error(e)

        metrics.track_loop()
        time.sleep(1)

