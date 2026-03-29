"""
Configuration module for the Mediation Remainder System
"""
import os
from datetime import datetime
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/data/mediation_system.db')

# Email configuration for notifications
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'sender_email': os.getenv('SENDER_EMAIL', 'your_email@gmail.com'),
    'sender_password': os.getenv('SENDER_PASSWORD', 'your_app_password'),
    'use_tls': os.getenv('USE_TLS', 'True').lower() == 'true',
}

# Notification settings
NOTIFICATION_SETTINGS = {
    'days_before_reminder': int(os.getenv('DAYS_BEFORE_REMINDER', 3)),
    'hours_before_reminder': int(os.getenv('HOURS_BEFORE_REMINDER', 24)),
    'enable_email': os.getenv('ENABLE_EMAIL', 'True').lower() == 'true',
    'enable_console': os.getenv('ENABLE_CONSOLE', 'True').lower() == 'true',
}

# Logging configuration
LOGGING_CONFIG = {
    'log_file': str(BASE_DIR / 'data' / 'mediation_system.log'),
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
}

# Application settings
APP_NAME = 'Mediation Remainder System'
APP_VERSION = '1.0.0'
