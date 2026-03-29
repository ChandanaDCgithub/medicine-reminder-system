"""
QUICK REFERENCE - Mediation Remainder System Commands
"""

╔══════════════════════════════════════════════════════════════════════════╗
║               MEDIATION REMAINDER SYSTEM - QUICK REFERENCE               ║
╚══════════════════════════════════════════════════════════════════════════╝

📋 INITIALIZATION
─────────────────────────────────────────────────────────────────────────
Command:    init_db
Purpose:    Initialize the database (run once at setup)
Example:    mediation> init_db

👤 MEDIATOR COMMANDS
─────────────────────────────────────────────────────────────────────────
Command:    add_mediator <name> <email> [phone] [expertise]
Purpose:    Add a new mediator
Example:    mediation> add_mediator "John Smith" john@medics.com 555-1234 "Family Law"

Command:    list_mediators
Purpose:    Display all registered mediators
Example:    mediation> list_mediators

Command:    show_mediator <mediator_id>
Purpose:    Show detailed information about a mediator
Example:    mediation> show_mediator 1

👥 PARTICIPANT COMMANDS
─────────────────────────────────────────────────────────────────────────
Command:    add_participant <name> <email> [phone] [party_type]
Purpose:    Add a new participant/party
Example:    mediation> add_participant "Jane Doe" jane@email.com 555-5678 "Party_A"

Command:    list_participants
Purpose:    Display all participants
Example:    mediation> list_participants

📅 SESSION COMMANDS
─────────────────────────────────────────────────────────────────────────
Command:    create_session <title> <mediator_id> <date(YYYY-MM-DD)> <time(HH:MM)>
Purpose:    Create a new mediation session
Example:    mediation> create_session "Case123" 1 2024-04-15 14:30

Command:    list_sessions
Purpose:    Display all mediation sessions
Example:    mediation> list_sessions

Command:    show_session <session_id>
Purpose:    Show detailed information about a session
Example:    mediation> show_session 1

Command:    add_participant_to_session <session_id> <participant_id>
Purpose:    Add a participant to a mediation session
Example:    mediation> add_participant_to_session 1 1

🔔 REMINDER COMMANDS
─────────────────────────────────────────────────────────────────────────
Command:    create_reminders <session_id>
Purpose:    Create reminder notifications for a session (3-day & 24-hour)
Example:    mediation> create_reminders 1

Command:    send_pending_reminders
Purpose:    Send all overdue reminders immediately
Example:    mediation> send_pending_reminders

Command:    list_session_reminders <session_id>
Purpose:    Show all reminders for a specific session
Example:    mediation> list_session_reminders 1

🛠️ UTILITY COMMANDS
─────────────────────────────────────────────────────────────────────────
Command:    help
Purpose:    Show all available commands
Example:    mediation> help

Command:    help <command>
Purpose:    Show detailed help for a specific command
Example:    mediation> help create_session

Command:    clear
Purpose:    Clear the screen
Example:    mediation> clear

Command:    exit (or quit)
Purpose:    Exit the application
Example:    mediation> exit

📊 TYPICAL WORKFLOW
─────────────────────────────────────────────────────────────────────────
1. add_mediator          ← Register a mediator
2. add_participant       ← Register one or more participants
3. create_session        ← Schedule a mediation session
4. add_participant_to_session  ← Link participants to session
5. create_reminders      ← Set up automatic reminders
6. send_pending_reminders ← Send reminders when due

🔧 ADVANCED SETUP
─────────────────────────────────────────────────────────────────────────
# Load demo data:
python demo_data.py

# Run background scheduler for automatic reminders:
python scheduler.py

# Run tests:
python -m pytest tests/

# Check logs:
tail -f data/mediation_system.log

📝 IMPORTANT NOTES
─────────────────────────────────────────────────────────────────────────
- Use YYYY-MM-DD format for dates
- Use HH:MM format (24-hour) for times
- Email addresses must be valid for notifications
- IDs are auto-generated (shown when items are created)
- All data is stored in data/mediation_system.db

🌐 CONFIGURATION
─────────────────────────────────────────────────────────────────────────
Edit .env file to customize:
- Database location
- Email server settings
- Reminder timing
- Notification methods
- Log level

📞 NEED HELP?
─────────────────────────────────────────────────────────────────────────
Type: help            (shows all commands)
Type: help <command>  (shows help for specific command)
Check: data/mediation_system.log (application logs)

═══════════════════════════════════════════════════════════════════════════
