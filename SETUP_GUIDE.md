"""
SETUP GUIDE - Mediation Remainder System
"""

# QUICK START GUIDE

## Step 1: Clone/Download the Project
- Download the project folder to your computer
- Navigate to: "mediation remainder system"

## Step 2: Create Python Virtual Environment
### Windows:
    python -m venv venv
    venv\Scripts\activate

### macOS/Linux:
    python3 -m venv venv
    source venv/bin/activate

## Step 3: Install Dependencies
    pip install -r requirements.txt

## Step 4: Configure Environment Variables
    - Copy .env.example to .env
    - Edit .env file with your settings
    - For Gmail:
      * Enable 2-Factor Authentication
      * Generate App Password
      * Add to .env: SENDER_PASSWORD=your_app_password

## Step 5: Create Database
    cd src
    python main.py
    mediation> init_db
    mediation> exit

## Step 6: Populate Demo Data (Optional)
    cd ..
    python demo_data.py

## Step 7: Start Using the System
    cd src
    python main.py

# DIRECTORY STRUCTURE

mediation-remainder-system/
├── src/                          # Main application code
│   ├── main.py                  # Application launcher
│   ├── cli.py                   # Command-line interface
│   ├── config.py                # Configuration settings
│   ├── models.py                # Database models
│   ├── database.py              # Database management
│   ├── people_manager.py        # Mediator/Participant mgmt
│   ├── session_manager.py       # Session management
│   ├── reminders.py             # Reminder service
│   └── notifications.py         # Notification handlers
│
├── tests/                       # Test files
│   └── test_basic.py           # Sample tests
│
├── data/                        # Data directory (created on first run)
│   ├── mediation_system.db     # SQLite database
│   ├── mediation_system.log    # Application logs
│   └── scheduler.log           # Scheduler logs
│
├── demo_data.py                # Script to load demo data
├── scheduler.py                # Background reminder scheduler
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Your local environment config (after setup)
└── README.md                 # Full documentation

# COMMON TASKS

## Add a Mediator
    mediation> add_mediator "John Doe" john@example.com 555-1234 "Family Law"

## Add a Participant
    mediation> add_participant "Jane Smith" jane@example.com 555-5678 "Party_A"

## Create a Session
    mediation> create_session "Case Title" 1 2024-04-15 14:30
    (Format: title mediator_id YYYY-MM-DD HH:MM)

## Add Participant to Session
    mediation> add_participant_to_session 1 1
    (session_id participant_id)

## Create Reminders
    mediation> create_reminders 1
    (Will create 3-day and 24-hour before reminders)

## Send Reminders Now
    mediation> send_pending_reminders

## View All Sessions
    mediation> list_sessions

## View Session Details
    mediation> show_session 1

## Get Help
    mediation> help
    mediation> help create_session

# EMAIL CONFIGURATION

### For Gmail:
1. Go to myaccount.google.com
2. Select Security from the left menu
3. Enable 2-Step Verification (if not already enabled)
4. Click "App passwords"
5. Select Mail and Windows Computer
6. Copy the generated 16-character password
7. In .env file, set:
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=<16-character-password>

### For Other Email Providers:
Contact your email provider for SMTP server details

# RUNNING THE SCHEDULER

To automatically send reminders in the background:

    python scheduler.py

This will:
- Check for pending reminders every 5 minutes
- Send due reminders automatically
- Log all activity to data/scheduler.log

# TROUBLESHOOTING

## Database errors
Solution: Run 'init_db' command again (will reset database)

## Import errors
Solution: Ensure virtual environment is activated and dependencies installed

## Email not sending
Solution: 
- Check .env configuration
- Enable CONSOLE notifications to test
- Check Gmail app password setup

## Can't find commands
Solution: Type 'help' to see all available commands

# NEXT STEPS

1. Add your mediators: add_mediator
2. Register participants: add_participant
3. Create sessions: create_session
4. Add people to sessions: add_participant_to_session
5. Create reminders: create_reminders
6. Send reminders: send_pending_reminders

# SUPPORT

Check logs in: data/mediation_system.log

"""

if __name__ == '__main__':
    print(__doc__)
