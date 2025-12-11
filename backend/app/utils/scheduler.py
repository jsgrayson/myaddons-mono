import schedule
import time

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
