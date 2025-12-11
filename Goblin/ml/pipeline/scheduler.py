"""
Automated scheduler for Goblin ML pipeline.
Runs hourly data collection and daily model retraining.
"""
import schedule
import time
import subprocess
import sys
from loguru import logger
from datetime import datetime

class GoblinScheduler:
    def __init__(self):
        self.project_root = "/app"  # Docker container path
        
    def run_ingestion(self):
        """Run hourly data ingestion."""
        try:
            logger.info("Starting scheduled data ingestion...")
            result = subprocess.run(
                [sys.executable, "-m", "ml.pipeline.ingest"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.success("Data ingestion completed successfully")
            else:
                logger.error(f"Data ingestion failed: {result.stderr}")
                self.send_error_alert("Data Ingestion", result.stderr)
                
        except Exception as e:
            logger.error(f"Data ingestion error: {e}")
            self.send_error_alert("Data Ingestion", str(e))
    
    def run_preprocessing(self):
        """Run data preprocessing."""
        try:
            logger.info("Starting data preprocessing...")
            result = subprocess.run(
                [sys.executable, "-m", "ml.pipeline.preprocess"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                logger.success("Preprocessing completed successfully")
                return True
            else:
                logger.error(f"Preprocessing failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Preprocessing error: {e}")
            return False
    
    def run_training(self):
        """Run model training (daily)."""
        try:
            logger.info("Starting scheduled model training...")
            
            # First preprocess
            if not self.run_preprocessing():
                logger.error("Skipping training due to preprocessing failure")
                return
            
            result = subprocess.run(
                [sys.executable, "-m", "ml.pipeline.train"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minute timeout
            )
            
            if result.returncode == 0:
                logger.success("Model training completed successfully")
            else:
                logger.error(f"Model training failed: {result.stderr}")
                self.send_error_alert("Model Training", result.stderr)
                
        except Exception as e:
            logger.error(f"Model training error: {e}")
            self.send_error_alert("Model Training", str(e))
    
    def run_predictions(self):
        """Run predictions and send alerts."""
        try:
            logger.info("Starting scheduled predictions...")
            result = subprocess.run(
                [sys.executable, "-m", "ml.pipeline.predict"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.success("Predictions completed successfully")
            else:
                logger.error(f"Predictions failed: {result.stderr}")
                self.send_error_alert("Predictions", result.stderr)
                
        except Exception as e:
            logger.error(f"Predictions error: {e}")
            self.send_error_alert("Predictions", str(e))
    
    def send_error_alert(self, task_name: str, error_message: str):
        """Send alert when a task fails."""
        try:
            from ml.pipeline.notifications import NotificationService
            notifier = NotificationService()
            
            discord_msg = f"⚠️ **{task_name} Failed**\n\n```\n{error_message[:500]}\n```"
            notifier.send_discord(discord_msg, f"Error: {task_name}")
            
            email_body = f"Goblin AI Task Failed\n\nTask: {task_name}\n\nError:\n{error_message}"
            notifier.send_email(f"Goblin Error: {task_name} Failed", email_body)
            
        except Exception as e:
            logger.error(f"Failed to send error alert: {e}")
    
    def start(self):
        """Start the scheduler."""
        logger.info("Starting Goblin Scheduler...")
        
        # Hourly: Data ingestion + predictions
        schedule.every().hour.do(self.run_ingestion)
        schedule.every().hour.at(":05").do(self.run_predictions)  # 5 min after ingestion
        
        # Daily: Model training at 3 AM
        schedule.every().day.at("03:00").do(self.run_training)
        
        logger.info("Scheduler configured:")
        logger.info("  - Hourly: Data ingestion + predictions")
        logger.info("  - Daily at 3 AM: Model retraining")
        
        # Run initial ingestion and prediction
        logger.info("Running initial ingestion...")
        self.run_ingestion()
        time.sleep(10)
        self.run_predictions()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    scheduler = GoblinScheduler()
    scheduler.start()
