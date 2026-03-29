"""
Mediation Session Management
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from models import MediationSession, Mediator, Participant
import logging

logger = logging.getLogger(__name__)


class SessionManager:
    """Manager for mediation sessions"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create_session(self, title: str, mediator_id: int, scheduled_date: datetime,
                      scheduled_time: str, description: str = None, case_number: str = None,
                      location: str = None, duration: int = 60, notes: str = None) -> Optional[MediationSession]:
        """Create a new mediation session"""
        
        # Verify mediator exists
        mediator = self.db_session.query(Mediator).filter_by(id=mediator_id).first()
        if not mediator:
            logger.error(f"Mediator {mediator_id} not found")
            return None
        
        session = MediationSession(
            title=title,
            mediator_id=mediator_id,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            description=description,
            case_number=case_number,
            location=location,
            estimated_duration=duration,
            notes=notes,
            status='Scheduled'
        )
        
        self.db_session.add(session)
        self.db_session.commit()
        
        logger.info(f"Created mediation session: {session.id}")
        return session
    
    def add_participant_to_session(self, session_id: int, participant_id: int) -> bool:
        """Add a participant to a session"""
        session = self.db_session.query(MediationSession).filter_by(id=session_id).first()
        participant = self.db_session.query(Participant).filter_by(id=participant_id).first()
        
        if not session or not participant:
            logger.error(f"Session {session_id} or Participant {participant_id} not found")
            return False
        
        if participant not in session.participants:
            session.participants.append(participant)
            self.db_session.commit()
            logger.info(f"Added participant {participant_id} to session {session_id}")
            return True
        
        return False
    
    def remove_participant_from_session(self, session_id: int, participant_id: int) -> bool:
        """Remove a participant from a session"""
        session = self.db_session.query(MediationSession).filter_by(id=session_id).first()
        participant = self.db_session.query(Participant).filter_by(id=participant_id).first()
        
        if not session or not participant:
            logger.error(f"Session {session_id} or Participant {participant_id} not found")
            return False
        
        if participant in session.participants:
            session.participants.remove(participant)
            self.db_session.commit()
            logger.info(f"Removed participant {participant_id} from session {session_id}")
            return True
        
        return False
    
    def get_session(self, session_id: int) -> Optional[MediationSession]:
        """Get a session by ID"""
        return self.db_session.query(MediationSession).filter_by(id=session_id).first()
    
    def get_all_sessions(self) -> List[MediationSession]:
        """Get all sessions"""
        return self.db_session.query(MediationSession).all()
    
    def get_sessions_for_mediator(self, mediator_id: int) -> List[MediationSession]:
        """Get all sessions for a specific mediator"""
        return self.db_session.query(MediationSession).filter_by(mediator_id=mediator_id).all()
    
    def get_sessions_for_participant(self, participant_id: int) -> List[MediationSession]:
        """Get all sessions for a specific participant"""
        return self.db_session.query(MediationSession).filter(
            MediationSession.participants.any(id=participant_id)
        ).all()
    
    def update_session(self, session_id: int, **kwargs) -> Optional[MediationSession]:
        """Update a session"""
        session = self.db_session.query(MediationSession).filter_by(id=session_id).first()
        
        if not session:
            logger.error(f"Session {session_id} not found")
            return None
        
        valid_fields = {'title', 'description', 'scheduled_date', 'scheduled_time',
                       'location', 'estimated_duration', 'status', 'notes'}
        
        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(session, key, value)
        
        session.updated_at = datetime.utcnow()
        self.db_session.commit()
        logger.info(f"Updated session {session_id}")
        
        return session
    
    def cancel_session(self, session_id: int, reason: str = None) -> Optional[MediationSession]:
        """Cancel a session"""
        session = self.db_session.query(MediationSession).filter_by(id=session_id).first()
        
        if not session:
            logger.error(f"Session {session_id} not found")
            return None
        
        session.status = 'Canceled'
        if reason:
            session.notes = f"Cancellation reason: {reason}"
        
        self.db_session.commit()
        logger.info(f"Canceled session {session_id}")
        
        return session
    
    def complete_session(self, session_id: int, summary: str = None) -> Optional[MediationSession]:
        """Mark a session as completed"""
        session = self.db_session.query(MediationSession).filter_by(id=session_id).first()
        
        if not session:
            logger.error(f"Session {session_id} not found")
            return None
        
        session.status = 'Completed'
        if summary:
            session.notes = f"{session.notes or ''}\nSession Summary: {summary}"
        
        self.db_session.commit()
        logger.info(f"Completed session {session_id}")
        
        return session
