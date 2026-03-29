"""
Sample test file for the Mediation Remainder System
Run with: python -m pytest tests/
"""
import pytest
from datetime import datetime, timedelta
from database import db, init_database
from people_manager import PeopleManager
from session_manager import SessionManager
from reminders import ReminderService
from models import Mediator, Participant, MediationSession


class TestPeopleManager:
    """Tests for PeopleManager"""
    
    def setup_method(self):
        """Setup test database"""
        # Use in-memory database for testing
        self.db = db
        self.db_session = self.db.get_session()
        self.people_mgr = PeopleManager(self.db_session)
    
    def teardown_method(self):
        """Cleanup test database"""
        self.db_session.close()
    
    def test_create_mediator(self):
        """Test creating a mediator"""
        mediator = self.people_mgr.create_mediator(
            "John Doe",
            "john@example.com",
            "555-1234",
            "Family"
        )
        
        assert mediator is not None
        assert mediator.name == "John Doe"
        assert mediator.email == "john@example.com"
    
    def test_get_mediator(self):
        """Test retrieving a mediator"""
        mediator = self.people_mgr.create_mediator(
            "Jane Smith",
            "jane@example.com"
        )
        
        retrieved = self.people_mgr.get_mediator(mediator.id)
        assert retrieved is not None
        assert retrieved.name == "Jane Smith"
    
    def test_create_participant(self):
        """Test creating a participant"""
        participant = self.people_mgr.create_participant(
            "Alice Johnson",
            "alice@example.com",
            "555-5678",
            "Party_A"
        )
        
        assert participant is not None
        assert participant.name == "Alice Johnson"
        assert participant.party_type == "Party_A"


class TestSessionManager:
    """Tests for SessionManager"""
    
    def setup_method(self):
        """Setup test database"""
        self.db = db
        self.db_session = self.db.get_session()
        self.people_mgr = PeopleManager(self.db_session)
        self.session_mgr = SessionManager(self.db_session)
    
    def teardown_method(self):
        """Cleanup test database"""
        self.db_session.close()
    
    def test_create_session(self):
        """Test creating a mediation session"""
        # Create mediator first
        mediator = self.people_mgr.create_mediator(
            "John Mediator",
            "john@example.com"
        )
        
        # Create session
        session = self.session_mgr.create_session(
            title="Test Case",
            mediator_id=mediator.id,
            scheduled_date=datetime.now() + timedelta(days=7),
            scheduled_time="14:00"
        )
        
        assert session is not None
        assert session.title == "Test Case"
        assert session.status == "Scheduled"
    
    def test_add_participant_to_session(self):
        """Test adding participant to session"""
        mediator = self.people_mgr.create_mediator(
            "John Mediator",
            "john@example.com"
        )
        
        participant = self.people_mgr.create_participant(
            "Bob Participant",
            "bob@example.com"
        )
        
        session = self.session_mgr.create_session(
            title="Test Case",
            mediator_id=mediator.id,
            scheduled_date=datetime.now() + timedelta(days=7),
            scheduled_time="14:00"
        )
        
        success = self.session_mgr.add_participant_to_session(session.id, participant.id)
        
        assert success is True
        assert len(session.participants) == 1


# Run with: python -m pytest tests/
if __name__ == '__main__':
    pytest.main([__file__])
