"""
Reminder management and scheduling for mediation sessions
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from models import MediationSession, Reminder, Participant
from notifications import NotificationManager
import logging

logger = logging.getLogger(__name__)


class ReminderService:
    """Service for managing reminders"""
    
    def __init__(self, db_session: Session, days_before: int = 3, hours_before: int = 24):
        self.db_session = db_session
        self.notification_manager = NotificationManager()
        self.days_before = days_before
        self.hours_before = hours_before
    
    def create_reminders_for_session(self, session_id: int, reminder_types: List[str] = None) -> List[Reminder]:
        """Create reminders for a mediation session"""
        if reminder_types is None:
            reminder_types = ['email', 'console']
        
        session = self.db_session.query(MediationSession).filter_by(id=session_id).first()
        if not session:
            logger.warning(f"Session {session_id} not found")
            return []
        
        reminders = []
        
        # Calculate reminder times
        session_datetime = datetime.combine(
            session.scheduled_date.date(),
            datetime.strptime(session.scheduled_time, '%H:%M').time() if session.scheduled_time else datetime.min.time()
        )
        
        # Create reminders at different intervals
        reminder_times = [
            session_datetime - timedelta(days=self.days_before),  # 3 days before
            session_datetime - timedelta(hours=self.hours_before),  # 24 hours before
        ]
        
        for reminder_type in reminder_types:
            for reminder_time in reminder_times:
                reminder = Reminder(
                    session_id=session_id,
                    reminder_type=reminder_type,
                    scheduled_time=reminder_time,
                    message=f"Reminder for mediation session: {session.title}"
                )
                self.db_session.add(reminder)
                reminders.append(reminder)
                logger.info(f"Created {reminder_type} reminder for session {session_id}")
        
        self.db_session.commit()
        return reminders
    
    def get_pending_reminders(self) -> List[Reminder]:
        """Get all reminders that are due to be sent"""
        now = datetime.utcnow()
        
        pending_reminders = self.db_session.query(Reminder).filter(
            Reminder.is_sent == False,
            Reminder.scheduled_time <= now
        ).all()
        
        return pending_reminders
    
    def send_pending_reminders(self) -> int:
        """Send all pending reminders and mark as sent"""
        pending = self.get_pending_reminders()
        sent_count = 0
        
        for reminder in pending:
            session = reminder.session
            
            # Get participants
            participants = self.db_session.query(Participant).join(
                MediationSession.participants
            ).filter(MediationSession.id == session.id).all()
            
            # Send reminder to each participant
            for participant in participants:
                success = self.notification_manager.send_reminder_notification(
                    participant_email=participant.email,
                    session_title=session.title,
                    scheduled_date=f"{session.scheduled_date.strftime('%Y-%m-%d')} {session.scheduled_time}",
                    location=session.location
                )
                
                if success:
                    sent_count += 1
            
            # Mark reminder as sent
            reminder.is_sent = True
            reminder.sent_at = datetime.utcnow()
            logger.info(f"Reminder {reminder.id} marked as sent")
        
        self.db_session.commit()
        return sent_count
    
    def reschedule_reminder(self, reminder_id: int, new_scheduled_time: datetime) -> Optional[Reminder]:
        """Reschedule a reminder"""
        reminder = self.db_session.query(Reminder).filter_by(id=reminder_id).first()
        
        if not reminder:
            logger.warning(f"Reminder {reminder_id} not found")
            return None
        
        reminder.scheduled_time = new_scheduled_time
        self.db_session.commit()
        logger.info(f"Reminder {reminder_id} rescheduled to {new_scheduled_time}")
        
        return reminder
    
    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete a reminder"""
        reminder = self.db_session.query(Reminder).filter_by(id=reminder_id).first()
        
        if not reminder:
            logger.warning(f"Reminder {reminder_id} not found")
            return False
        
        self.db_session.delete(reminder)
        self.db_session.commit()
        logger.info(f"Reminder {reminder_id} deleted")
        
        return True
    
    def get_session_reminders(self, session_id: int) -> List[Reminder]:
        """Get all reminders for a specific session"""
        return self.db_session.query(Reminder).filter_by(session_id=session_id).all()
