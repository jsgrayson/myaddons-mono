import time
from agents.common.agent_metrics_template import AgentMetrics

metrics = AgentMetrics("ml_worker")

def run_ml_worker():
    while True:
        try:
            # Example: tasks in ML queue
            task_queue = []
            metrics.set_queue_depth(len(task_queue))

            # MAIN LOGIC
            # ml_training_tasks()
            # YOUR LOGIC HERE

            # Example:
            # metrics.job_completed()

        except Exception as e:
            metrics.error(e)

        metrics.track_loop()
        time.sleep(1)

