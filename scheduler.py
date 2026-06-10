import schedule
import time
from datetime import datetime
from main import run_dashboard
import logging
import os
os.makedirs("logs", exist_ok=True)

# Configure logging 
logging.basicConfig(filename='logs/scheduler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scheduled_task():
    try:
        logging.info("Starting scheduled dashboard run.")
        run_dashboard()
        logging.info("Dashboard run completed successfully.")
    except Exception as e:
        logging.error(f"Error during dashboard run: {e}")

def start_scheduler():
    # Schedule the task to run on the 1st of every day at 8:00 AM
    schedule.every().day.at("08:00").do(scheduled_task)
    logging.info("Scheduler started. Dashboard will run on the 1st of every day at 8:00 AM.")
    print("Scheduler running... (Ctrl+C to stop)")

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    start_scheduler()