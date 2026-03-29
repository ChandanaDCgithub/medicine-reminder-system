"""
Database initialization and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL
from models import Base


class Database:
    """Database manager"""
    
    def __init__(self, database_url: str = DATABASE_URL):
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_all(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
        print("Database tables created successfully!")
    
    def drop_all(self):
        """Drop all tables"""
        Base.metadata.drop_all(bind=self.engine)
        print("All database tables dropped!")
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()


# Global database instance
db = Database()


def init_database():
    """Initialize the database"""
    db.create_all()
