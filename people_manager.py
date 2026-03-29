"""
Management of mediators and participants
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Mediator, Participant
import logging

logger = logging.getLogger(__name__)


class PeopleManager:
    """Manager for mediators and participants"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    # Mediator methods
    def create_mediator(self, name: str, email: str, phone: str = None,
                       expertise: str = None) -> Optional[Mediator]:
        """Create a new mediator"""
        
        # Check if email already exists
        existing = self.db_session.query(Mediator).filter_by(email=email).first()
        if existing:
            logger.warning(f"Mediator with email {email} already exists")
            return None
        
        mediator = Mediator(
            name=name,
            email=email,
            phone=phone,
            expertise=expertise
        )
        
        self.db_session.add(mediator)
        self.db_session.commit()
        
        logger.info(f"Created mediator: {mediator.id} - {name}")
        return mediator
    
    def get_mediator(self, mediator_id: int) -> Optional[Mediator]:
        """Get a mediator by ID"""
        return self.db_session.query(Mediator).filter_by(id=mediator_id).first()
    
    def get_all_mediators(self) -> List[Mediator]:
        """Get all mediators"""
        return self.db_session.query(Mediator).all()
    
    def get_mediators_by_expertise(self, expertise: str) -> List[Mediator]:
        """Get mediators by expertise"""
        return self.db_session.query(Mediator).filter_by(expertise=expertise).all()
    
    def update_mediator(self, mediator_id: int, **kwargs) -> Optional[Mediator]:
        """Update mediator information"""
        mediator = self.db_session.query(Mediator).filter_by(id=mediator_id).first()
        
        if not mediator:
            logger.error(f"Mediator {mediator_id} not found")
            return None
        
        valid_fields = {'name', 'email', 'phone', 'expertise'}
        
        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(mediator, key, value)
        
        self.db_session.commit()
        logger.info(f"Updated mediator {mediator_id}")
        
        return mediator
    
    def delete_mediator(self, mediator_id: int) -> bool:
        """Delete a mediator"""
        mediator = self.db_session.query(Mediator).filter_by(id=mediator_id).first()
        
        if not mediator:
            logger.error(f"Mediator {mediator_id} not found")
            return False
        
        self.db_session.delete(mediator)
        self.db_session.commit()
        logger.info(f"Deleted mediator {mediator_id}")
        
        return True
    
    # Participant methods
    def create_participant(self, name: str, email: str, phone: str = None,
                          party_type: str = None) -> Optional[Participant]:
        """Create a new participant"""
        
        participant = Participant(
            name=name,
            email=email,
            phone=phone,
            party_type=party_type
        )
        
        self.db_session.add(participant)
        self.db_session.commit()
        
        logger.info(f"Created participant: {participant.id} - {name}")
        return participant
    
    def get_participant(self, participant_id: int) -> Optional[Participant]:
        """Get a participant by ID"""
        return self.db_session.query(Participant).filter_by(id=participant_id).first()
    
    def get_all_participants(self) -> List[Participant]:
        """Get all participants"""
        return self.db_session.query(Participant).all()
    
    def get_participants_by_party_type(self, party_type: str) -> List[Participant]:
        """Get participants by party type"""
        return self.db_session.query(Participant).filter_by(party_type=party_type).all()
    
    def update_participant(self, participant_id: int, **kwargs) -> Optional[Participant]:
        """Update participant information"""
        participant = self.db_session.query(Participant).filter_by(id=participant_id).first()
        
        if not participant:
            logger.error(f"Participant {participant_id} not found")
            return None
        
        valid_fields = {'name', 'email', 'phone', 'party_type'}
        
        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(participant, key, value)
        
        self.db_session.commit()
        logger.info(f"Updated participant {participant_id}")
        
        return participant
    
    def delete_participant(self, participant_id: int) -> bool:
        """Delete a participant"""
        participant = self.db_session.query(Participant).filter_by(id=participant_id).first()
        
        if not participant:
            logger.error(f"Participant {participant_id} not found")
            return False
        
        self.db_session.delete(participant)
        self.db_session.commit()
        logger.info(f"Deleted participant {participant_id}")
        
        return True
