"""
Database models for the Mediation Remainder System
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Mediator(Base):
    """Mediator model"""
    __tablename__ = 'mediators'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    expertise = Column(String(255))  # e.g., Family, Commercial, Labor
    created_at = Column(DateTime, default=datetime.utcnow)
    
    mediation_sessions = relationship('MediationSession', back_populates='mediator', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Mediator {self.name}>'


class Participant(Base):
    """Participant model"""
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    party_type = Column(String(50))  # Party A, Party B, Observer, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sessions = relationship('MediationSession', secondary='session_participants', back_populates='participants')

    def __repr__(self):
        return f'<Participant {self.name}>'


class MediationSession(Base):
    """Mediation Session model"""
    __tablename__ = 'mediation_sessions'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    case_number = Column(String(50), unique=True)
    mediator_id = Column(Integer, ForeignKey('mediators.id'), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    scheduled_time = Column(String(10))  # Format: HH:MM
    estimated_duration = Column(Integer)  # in minutes
    location = Column(String(255))
    status = Column(String(50), default='Scheduled')  # Scheduled, In Progress, Completed, Canceled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    mediator = relationship('Mediator', back_populates='mediation_sessions')
    participants = relationship('Participant', secondary='session_participants', back_populates='sessions')
    reminders = relationship('Reminder', back_populates='session', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<MediationSession {self.title} - {self.scheduled_date}>'


class SessionParticipant(Base):
    """Association table for sessions and participants"""
    __tablename__ = 'session_participants'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('mediation_sessions.id'), nullable=False)
    participant_id = Column(Integer, ForeignKey('participants.id'), nullable=False)


class Reminder(Base):
    """Reminder model"""
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('mediation_sessions.id'), nullable=False)
    reminder_type = Column(String(50))  # email, sms, console, etc.
    scheduled_time = Column(DateTime, nullable=False)
    message = Column(Text)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship('MediationSession', back_populates='reminders')

    def __repr__(self):
        return f'<Reminder {self.reminder_type} - {self.scheduled_time}>'
