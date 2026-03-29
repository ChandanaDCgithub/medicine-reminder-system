"""
Notification handlers for the Mediation Remainder System
Supports email and console notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List
from config import EMAIL_CONFIG, NOTIFICATION_SETTINGS
import logging

logger = logging.getLogger(__name__)


class NotificationHandler:
    """Base notification handler"""
    
    def send(self, recipient: str, subject: str, message: str) -> bool:
        raise NotImplementedError


class EmailNotificationHandler(NotificationHandler):
    """Email notification handler"""
    
    def __init__(self, config=None):
        self.config = config or EMAIL_CONFIG
    
    def send(self, recipient: str, subject: str, message: str) -> bool:
        """Send email notification"""
        try:
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            
            if self.config['use_tls']:
                server.starttls()
            
            server.login(self.config['sender_email'], self.config['sender_password'])
            
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'html'))
            
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent to {recipient}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {str(e)}")
            return False


class ConsoleNotificationHandler(NotificationHandler):
    """Console notification handler for development/testing"""
    
    def send(self, recipient: str, subject: str, message: str) -> bool:
        """Print notification to console"""
        try:
            print(f"\n{'='*60}")
            print(f"NOTIFICATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")
            print(f"To: {recipient}")
            print(f"Subject: {subject}")
            print(f"{'='*60}")
            print(message)
            print(f"{'='*60}\n")
            
            logger.info(f"Console notification displayed for {recipient}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to display console notification: {str(e)}")
            return False


class NotificationManager:
    """Manages multiple notification handlers"""
    
    def __init__(self):
        self.handlers: List[NotificationHandler] = []
        self._initialize_handlers()
    
    def _initialize_handlers(self):
        """Initialize configured notification handlers"""
        if NOTIFICATION_SETTINGS['enable_email']:
            self.handlers.append(EmailNotificationHandler())
        
        if NOTIFICATION_SETTINGS['enable_console']:
            self.handlers.append(ConsoleNotificationHandler())
    
    def send_notification(self, recipient: str, subject: str, message: str) -> bool:
        """Send notification through all configured handlers"""
        results = []
        
        for handler in self.handlers:
            try:
                result = handler.send(recipient, subject, message)
                results.append(result)
            except Exception as e:
                logger.error(f"Error in notification handler: {str(e)}")
                results.append(False)
        
        return any(results)  # Return True if at least one handler succeeded
    
    def send_reminder_notification(self, participant_email: str, session_title: str, 
                                  scheduled_date: str, location: str = None) -> bool:
        """Send mediation reminder notification"""
        subject = f"Mediation Session Reminder: {session_title}"
        
        message = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Mediation Session Reminder</h2>
                <p>Dear Participant,</p>
                <p>This is a reminder about your upcoming mediation session:</p>
                
                <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px;">
                    <p><strong>Session Title:</strong> {session_title}</p>
                    <p><strong>Scheduled Date & Time:</strong> {scheduled_date}</p>
                    {f'<p><strong>Location:</strong> {location}</p>' if location else ''}
                </div>
                
                <p>Please ensure you arrive 10 minutes early.</p>
                <p>If you have any questions or need to reschedule, please contact your mediator.</p>
                
                <br>
                <p>Best regards,<br>
                Mediation System</p>
            </body>
        </html>
        """
        
        return self.send_notification(participant_email, subject, message)
