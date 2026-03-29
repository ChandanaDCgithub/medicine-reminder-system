"""
Medicine Reminder System - Updated Models
Extended database models for user authentication and medicine management
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Time, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(Base):
    """User model with authentication"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150))
    age = Column(Integer)
    medical_history = Column(Text)
    emergency_contact = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    medicines = relationship('Medicine', back_populates='user', cascade='all, delete-orphan')
    schedules = relationship('MedicineSchedule', back_populates='user', cascade='all, delete-orphan')
    medicine_history = relationship('MedicineHistory', back_populates='user', cascade='all, delete-orphan')
    water_logs = relationship('WaterLog', back_populates='user', cascade='all, delete-orphan')
    missed_alerts = relationship('MissedMedicineAlert', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Medicine(Base):
    """Medicine model"""
    __tablename__ = 'medicines'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(200), nullable=False)
    dosage = Column(String(100))  # e.g., "500mg", "2 tablets"
    description = Column(Text)
    reason = Column(String(255))  # e.g., "Headache", "Blood pressure"
    manufacturer = Column(String(150))
    batch_number = Column(String(100))
    expiry_date = Column(DateTime)
    side_effects = Column(Text)
    instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='medicines')
    schedules = relationship('MedicineSchedule', back_populates='medicine', cascade='all, delete-orphan')
    history = relationship('MedicineHistory', back_populates='medicine', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Medicine {self.name}>'


class MedicineSchedule(Base):
    """Medicine schedule model (morning/afternoon/evening)"""
    __tablename__ = 'medicine_schedules'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    medicine_id = Column(Integer, ForeignKey('medicines.id'), nullable=False)
    
    # Time slots
    morning_time = Column(String(10))  # HH:MM format
    afternoon_time = Column(String(10))
    evening_time = Column(String(10))
    night_time = Column(String(10))
    
    # Dosage per slot
    morning_dosage = Column(String(100))
    afternoon_dosage = Column(String(100))
    evening_dosage = Column(String(100))
    night_dosage = Column(String(100))
    
    # Days of week (comma-separated: Mon,Tue,Wed,Thu,Fri,Sat,Sun)
    frequency = Column(String(50))  # "Daily", "Alternate", "Specific days", etc.
    days = Column(String(100))  # Specific days if needed
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)  # Null if ongoing
    
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='schedules')
    medicine = relationship('Medicine', back_populates='schedules')
    history = relationship('MedicineHistory', back_populates='schedule', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<MedicineSchedule {self.medicine.name}>'


class MedicineHistory(Base):
    """Track medicine consumption"""
    __tablename__ = 'medicine_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    medicine_id = Column(Integer, ForeignKey('medicines.id'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('medicine_schedules.id'), nullable=False)
    
    scheduled_time = Column(DateTime, nullable=False)
    taken_time = Column(DateTime)  # When actually taken
    taken = Column(Boolean, default=False)
    dosage = Column(String(100))
    
    time_slot = Column(String(20))  # 'morning', 'afternoon', 'evening', 'night'
    notes = Column(Text)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='medicine_history')
    medicine = relationship('Medicine', back_populates='history')
    schedule = relationship('MedicineSchedule', back_populates='history')

    def __repr__(self):
        return f'<MedicineHistory {self.medicine.name} - {self.scheduled_time}>'


class WaterLog(Base):
    """Track water intake reminders"""
    __tablename__ = 'water_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    scheduled_time = Column(DateTime, nullable=False)
    logged_time = Column(DateTime)  # When water was logged
    logged = Column(Boolean, default=False)
    
    amount_ml = Column(Float)  # Amount of water in milliliters
    reminder_sent = Column(Boolean, default=False)
    reminder_sent_at = Column(DateTime)
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='water_logs')

    def __repr__(self):
        return f'<WaterLog {self.user.username} - {self.scheduled_time}>'


class MissedMedicineAlert(Base):
    """Alert when medicine is missed"""
    __tablename__ = 'missed_medicine_alerts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    medicine_id = Column(Integer, ForeignKey('medicines.id'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('medicine_schedules.id'), nullable=False)
    
    medicine_history_id = Column(Integer, ForeignKey('medicine_history.id'))
    
    scheduled_time = Column(DateTime, nullable=False)
    time_slot = Column(String(20))  # 'morning', 'afternoon', 'evening', 'night'
    
    alert_sent = Column(Boolean, default=False)
    alert_sent_at = Column(DateTime)
    alert_acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime)
    
    reason = Column(Text)  # Why was it missed?
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='missed_alerts')
    medicine = relationship('Medicine')
    schedule = relationship('MedicineSchedule')

    def __repr__(self):
        return f'<MissedAlert {self.medicine.name} - {self.scheduled_time}>'
