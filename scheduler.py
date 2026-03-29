"""
Scheduler script for running reminders automatically
Run this in the background to send reminders at scheduled times
python scheduler.py
"""
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from database import db
from reminders import ReminderService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_scheduler(check_interval=300):
    """
    Run the reminder scheduler
    
    Args:
        check_interval: Seconds between checks (default: 5 minutes)
    """
    
    logger.info("Mediation Remainder System Scheduler Started")
    logger.info(f"Check interval: {check_interval} seconds")
    
    print("\n" + "="*60)
    print("Mediation Reminder Scheduler")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Check interval: {check_interval} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            try:
                # Get database session
                db_session = db.get_session()
                reminder_svc = ReminderService(db_session)
                
                # Check and send pending reminders
                pending = reminder_svc.get_pending_reminders()
                
                if pending:
                    logger.info(f"Found {len(pending)} pending reminders")
                    count = reminder_svc.send_pending_reminders()
                    logger.info(f"Sent {count} reminders")
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent {count} reminders")
                else:
                    logger.debug("No pending reminders")
                
                db_session.close()
                
            except Exception as e:
                logger.error(f"Error processing reminders: {e}")
                print(f"Error: {e}")
            
            # Wait before next check
            time.sleep(check_interval)
    
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        print("\n\nScheduler stopped.")


if __name__ == '__main__':
    # Run scheduler (check every 5 minutes / 300 seconds)
    run_scheduler(check_interval=300)
