"""
Command-line interface for the Mediation Remainder System
"""
import cmd
from datetime import datetime, timedelta
from typing import Optional
from database import db
from people_manager import PeopleManager
from session_manager import SessionManager
from reminders import ReminderService
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)


class MediationCLI(cmd.Cmd):
    """Interactive CLI for the Mediation Remainder System"""
    
    intro = """
    ╔════════════════════════════════════════════════════════════╗
    ║   Welcome to the Mediation Remainder System                ║
    ║   Type 'help' for available commands                       ║
    ╚════════════════════════════════════════════════════════════╝
    """
    
    prompt = "mediation> "
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_session = db.get_session()
        self.people_mgr = PeopleManager(self.db_session)
        self.session_mgr = SessionManager(self.db_session)
        self.reminder_svc = ReminderService(self.db_session)
    
    def do_init_db(self, _):
        """Initialize the database: init_db"""
        db.create_all()
        print("✓ Database initialized successfully!")
    
    # ==================== MEDIATOR COMMANDS ====================
    
    def do_add_mediator(self, args):
        """Add a new mediator: add_mediator <name> <email> [phone] [expertise]"""
        parts = args.split()
        if len(parts) < 2:
            print("❌ Usage: add_mediator <name> <email> [phone] [expertise]")
            return
        
        name = parts[0]
        email = parts[1]
        phone = parts[2] if len(parts) > 2 else None
        expertise = parts[3] if len(parts) > 3 else None
        
        mediator = self.people_mgr.create_mediator(name, email, phone, expertise)
        if mediator:
            print(f"✓ Mediator created: ID={mediator.id}, Name={mediator.name}")
        else:
            print("❌ Failed to create mediator")
    
    def do_list_mediators(self, _):
        """List all mediators: list_mediators"""
        mediators = self.people_mgr.get_all_mediators()
        
        if not mediators:
            print("No mediators found.")
            return
        
        print(f"\n{'ID':<5} {'Name':<25} {'Email':<30} {'Expertise':<20}")
        print("-" * 80)
        for m in mediators:
            print(f"{m.id:<5} {m.name:<25} {m.email:<30} {m.expertise or 'N/A':<20}")
        print()
    
    def do_show_mediator(self, args):
        """Show mediator details: show_mediator <mediator_id>"""
        try:
            mediator_id = int(args.strip())
            mediator = self.people_mgr.get_mediator(mediator_id)
            
            if not mediator:
                print(f"❌ Mediator {mediator_id} not found")
                return
            
            print(f"\n{'='*50}")
            print(f"Mediator ID: {mediator.id}")
            print(f"Name: {mediator.name}")
            print(f"Email: {mediator.email}")
            print(f"Phone: {mediator.phone or 'N/A'}")
            print(f"Expertise: {mediator.expertise or 'N/A'}")
            print(f"Created: {mediator.created_at}")
            print(f"Sessions: {len(mediator.mediation_sessions)}")
            print(f"{'='*50}\n")
        
        except ValueError:
            print("❌ Invalid mediator ID")
    
    # ==================== PARTICIPANT COMMANDS ====================
    
    def do_add_participant(self, args):
        """Add a new participant: add_participant <name> <email> [phone] [party_type]"""
        parts = args.split()
        if len(parts) < 2:
            print("❌ Usage: add_participant <name> <email> [phone] [party_type]")
            return
        
        name = parts[0]
        email = parts[1]
        phone = parts[2] if len(parts) > 2 else None
        party_type = parts[3] if len(parts) > 3 else None
        
        participant = self.people_mgr.create_participant(name, email, phone, party_type)
        if participant:
            print(f"✓ Participant created: ID={participant.id}, Name={participant.name}")
        else:
            print("❌ Failed to create participant")
    
    def do_list_participants(self, _):
        """List all participants: list_participants"""
        participants = self.people_mgr.get_all_participants()
        
        if not participants:
            print("No participants found.")
            return
        
        print(f"\n{'ID':<5} {'Name':<25} {'Email':<30} {'Party Type':<15}")
        print("-" * 75)
        for p in participants:
            print(f"{p.id:<5} {p.name:<25} {p.email:<30} {p.party_type or 'N/A':<15}")
        print()
    
    # ==================== SESSION COMMANDS ====================
    
    def do_create_session(self, args):
        """Create mediation session: create_session <title> <mediator_id> <date(YYYY-MM-DD)> <time(HH:MM)>"""
        parts = args.split(maxsplit=3)
        if len(parts) < 4:
            print("❌ Usage: create_session <title> <mediator_id> <date(YYYY-MM-DD)> <time(HH:MM)>")
            return
        
        try:
            title = parts[0]
            mediator_id = int(parts[1])
            date_str = parts[2]
            time_str = parts[3]
            
            scheduled_date = datetime.strptime(date_str, '%Y-%m-%d')
            
            session = self.session_mgr.create_session(
                title=title,
                mediator_id=mediator_id,
                scheduled_date=scheduled_date,
                scheduled_time=time_str
            )
            
            if session:
                print(f"✓ Session created: ID={session.id}, Title={session.title}")
            else:
                print("❌ Failed to create session")
        
        except (ValueError, IndexError):
            print("❌ Invalid input format")
    
    def do_list_sessions(self, _):
        """List all sessions: list_sessions"""
        sessions = self.session_mgr.get_all_sessions()
        
        if not sessions:
            print("No sessions found.")
            return
        
        print(f"\n{'ID':<5} {'Title':<30} {'Date':<12} {'Time':<8} {'Status':<12}")
        print("-" * 67)
        for s in sessions:
            date_str = s.scheduled_date.strftime('%Y-%m-%d')
            print(f"{s.id:<5} {s.title:<30} {date_str:<12} {s.scheduled_time:<8} {s.status:<12}")
        print()
    
    def do_show_session(self, args):
        """Show session details: show_session <session_id>"""
        try:
            session_id = int(args.strip())
            session = self.session_mgr.get_session(session_id)
            
            if not session:
                print(f"❌ Session {session_id} not found")
                return
            
            print(f"\n{'='*60}")
            print(f"Session ID: {session.id}")
            print(f"Title: {session.title}")
            print(f"Mediator: {session.mediator.name}")
            print(f"Date: {session.scheduled_date.strftime('%Y-%m-%d')}")
            print(f"Time: {session.scheduled_time}")
            print(f"Status: {session.status}")
            print(f"Location: {session.location or 'N/A'}")
            print(f"Duration: {session.estimated_duration} minutes")
            print(f"Participants: {len(session.participants)}")
            if session.participants:
                for p in session.participants:
                    print(f"  - {p.name} ({p.email})")
            print(f"{'='*60}\n")
        
        except ValueError:
            print("❌ Invalid session ID")
    
    def do_add_participant_to_session(self, args):
        """Add participant to session: add_participant_to_session <session_id> <participant_id>"""
        parts = args.split()
        if len(parts) < 2:
            print("❌ Usage: add_participant_to_session <session_id> <participant_id>")
            return
        
        try:
            session_id = int(parts[0])
            participant_id = int(parts[1])
            
            success = self.session_mgr.add_participant_to_session(session_id, participant_id)
            if success:
                print("✓ Participant added to session")
            else:
                print("❌ Failed to add participant")
        
        except ValueError:
            print("❌ Invalid IDs")
    
    # ==================== REMINDER COMMANDS ====================
    
    def do_create_reminders(self, args):
        """Create reminders for session: create_reminders <session_id>"""
        try:
            session_id = int(args.strip())
            reminders = self.reminder_svc.create_reminders_for_session(
                session_id,
                reminder_types=['email', 'console']
            )
            print(f"✓ Created {len(reminders)} reminders for session {session_id}")
        
        except ValueError:
            print("❌ Invalid session ID")
    
    def do_send_pending_reminders(self, _):
        """Send all pending reminders: send_pending_reminders"""
        count = self.reminder_svc.send_pending_reminders()
        print(f"✓ Sent {count} reminders")
    
    def do_list_session_reminders(self, args):
        """List reminders for a session: list_session_reminders <session_id>"""
        try:
            session_id = int(args.strip())
            reminders = self.reminder_svc.get_session_reminders(session_id)
            
            if not reminders:
                print(f"No reminders for session {session_id}")
                return
            
            print(f"\n{'ID':<5} {'Type':<10} {'Scheduled Time':<20} {'Sent':<5}")
            print("-" * 40)
            for r in reminders:
                sent_status = "✓" if r.is_sent else "✗"
                print(f"{r.id:<5} {r.reminder_type:<10} {str(r.scheduled_time):<20} {sent_status:<5}")
            print()
        
        except ValueError:
            print("❌ Invalid session ID")
    
    # ==================== UTILITY COMMANDS ====================
    
    def do_clear_screen(self, _):
        """Clear the screen: clear"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def do_help(self, args):
        """List available commands or get help for a command"""
        if args:
            super().do_help(args)
        else:
            print("""
    Available Commands:
    
    DATABASE:
      init_db                           - Initialize the database
    
    MEDIATORS:
      add_mediator <name> <email> ...   - Add new mediator
      list_mediators                    - List all mediators
      show_mediator <id>                - Show mediator details
    
    PARTICIPANTS:
      add_participant <name> <email>... - Add new participant
      list_participants                 - List all participants
    
    SESSIONS:
      create_session <title> <med_id>...- Create mediation session
      list_sessions                     - List all sessions
      show_session <id>                 - Show session details
      add_participant_to_session <s> <p>- Add participant to session
    
    REMINDERS:
      create_reminders <session_id>     - Create reminders for session
      send_pending_reminders            - Send all pending reminders
      list_session_reminders <id>       - List reminders for session
    
    OTHER:
      help [command]                    - Show this help or command help
      clear                             - Clear the screen
      exit                             - Exit the application
            """)
    
    def do_exit(self, _):
        """Exit the application: exit"""
        self.db_session.close()
        db.close()
        print("Goodbye!")
        return True
    
    do_quit = do_exit


def main():
    """Run the CLI"""
    cli = MediationCLI()
    cli.cmdloop()


if __name__ == '__main__':
    main()
