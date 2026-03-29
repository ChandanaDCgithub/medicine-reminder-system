"""
ARCHITECTURE OVERVIEW - Mediation Remainder System
System Design and Component Structure
"""

╔══════════════════════════════════════════════════════════════════════════╗
║                        SYSTEM ARCHITECTURE                               ║
║              Mediation Remainder System v1.0.0                           ║
╚══════════════════════════════════════════════════════════════════════════╝

HIGH-LEVEL ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────┐
    │              USER INTERFACE LAYER                            │
    │              (CLI - Interactive Commands)                   │
    │                    (cli.py)                                 │
    └──────────────────┬──────────────────────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────────────────┐
    │         BUSINESS LOGIC LAYER                                 │
    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
    │  │ People   │ │ Session  │ │ Reminder │ │Notification
    │  │ Manager  │ │ Manager  │ │ Service  │ │ Handler  │       │
    │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
    │  (people_  (session_   (reminders.py) (notifications.py)   │
    │   manager)  manager)                                        │
    └──────────────────┬──────────────────────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────────────────┐
    │          DATA ACCESS LAYER                                   │
    │  ┌──────────────────────────────────────┐                   │
    │  │    Database Module (database.py)     │                   │
    │  │    Models Module (models.py)         │                   │
    │  └──────────────────────────────────────┘                   │
    └──────────────────┬──────────────────────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────────────────┐
    │          PERSISTENT STORAGE LAYER                            │
    │  ┌──────────────────────────────────────┐                   │
    │  │  SQLite Database (SQLAlchemy ORM)    │                   │
    │  │  mediation_system.db                 │                   │
    │  └──────────────────────────────────────┘                   │
    └──────────────────────────────────────────────────────────────┘

DATA FLOW DIAGRAM
═══════════════════════════════════════════════════════════════════════════

User Input (CLI)
      │
      ▼
   CLI Parser
      │
      ├─────────────────────────────────┐
      │                                  │
      ▼                                  ▼
 People Manager              Session Manager      Reminder Service
      │                            │                    │
      ├──────────────────┬─────────┴────┬───────────────┤
      │                  │              │               │
   Create/Update      Create/Update  Schedule      Process/Send
   Mediators &        Sessions     Notifications   Reminders
   Participants
      │                  │              │               │
      └──────────┬───────┴──────────────┴───────────────┘
                 │
                 ▼
          Database Models
          (SQLAlchemy)
                 │
                 ▼
          SQLite Database
                 │
                 ▼
          Data Persistence

DATABASE SCHEMA
═══════════════════════════════════════════════════════════════════════════

┌─────────────────┐
│   MEDIATORS     │
├─────────────────┤
│ id (PK)         │
│ name            │
│ email (UNIQUE)  │
│ phone           │
│ expertise       │
│ created_at      │
└────────┬────────┘
         │
    ┌────▼─────────────────────┐
    │ leads (1:N)              │
    │                          │
    └────────────┬─────────────┘
                 │
    ┌────────────▼───────────┐
    │MEDIATION_SESSIONS      │
    ├────────────────────────┤
    │ id (PK)                │
    │ title                  │
    │ mediator_id (FK)       │
    │ scheduled_date         │
    │ scheduled_time         │
    │ location               │
    │ status                 │
    │ created_at             │
    │ updated_at             │
    └────────────┬───────────┘
         ┌───────┴────────────┐
         │ has reminders (1:N)│
         │ has participants(M:N)
         │                    │
    ┌────▼────────┐    ┌──────▼──────────┐
    │  REMINDERS  │    │SESSION_PARTICIPANTS
    ├─────────────┤    ├─────────────────┤
    │ id (PK)     │    │session_id (FK)  │
    │ session_id  │    │participant_id(FK
    │ reminder_   │    └────────┬────────┘
    │   type      │             │
    │ scheduled   │             │
    │   _time     │             │
    │ is_sent     │    ┌────────▼──────────┐
    │ sent_at     │    │  PARTICIPANTS     │
    └─────────────┘    ├───────────────────┤
                       │ id (PK)           │
                       │ name              │
                       │ email             │
                       │ phone             │
                       │ party_type        │
                       │ created_at        │
                       └───────────────────┘

KEY ENTITIES RELATIONSHIPS
═══════════════════════════════════════════════════════════════════════════

Mediator 1──────M MediationSession
  │                      │
  │                      │
  └──────[leads]─────────┘
  
Mediator: Has zero or more sessions
Session: Led by exactly one mediator

MediationSession M──────M Participant
              [via SessionParticipant junction table]

Session: Has zero or more participants
Participant: Participates in zero or more sessions

MediationSession 1──────M Reminder

Session: Has zero or more reminders
Reminder: Belongs to exactly one session


MODULE RESPONSIBILITIES
═══════════════════════════════════════════════════════════════════════════

main.py
───────
• Entry point for the application
• Initializes database
• Launches CLI interface
• Handles logging configuration

cli.py (450+ lines)
───────────────────
• Interactive command-line interface
• Command parsing and execution
• User input validation
• Output formatting and display
• Help system

config.py
─────────
• Environment variable management
• Configuration defaults
• Database URL configuration
• Email settings
• Notification preferences
• Logging configuration

models.py
─────────
• SQLAlchemy ORM models
• Database table definitions
• Model relationships
• Data validation constraints

database.py
───────────
• Database engine initialization
• Session factory setup
• Table creation/deletion
• Session management utilities

people_manager.py
─────────────────
• Mediator CRUD operations (Create, Read, Update, Delete)
• Participant CRUD operations
• Query and filter operations
• Validation and error handling

session_manager.py
──────────────────
• Session creation and management
• Participant assignment to sessions
• Session status tracking
• Session updates and completion

reminders.py
────────────
• Reminder creation logic
• Pending reminder detection
• Reminder sending orchestration
• Reminder rescheduling
• Reminder deletion

notifications.py
────────────────
• Email notification handler
• Console notification handler
• Notification manager (multi-handler)
• Custom message formatting

scheduler.py
───────────
• Background scheduling loop
• Periodic pending reminder checks
• Automatic reminder sending
• Error handling and logging

demo_data.py
────────────
• Sample data population
• Test case creation
• Demo environment setup

CONFIG FLOW
═══════════════════════════════════════════════════════════════════════════

.env File
   ↓
config.py (reads environment variables)
   ↓
Database (from DATABASE_URL)
Email (SMTP settings)
Notifications (timing, handlers)
Logging (level, file)
   ↓
Applied throughout application

NOTIFICATION FLOW
═══════════════════════════════════════════════════════════════════════════

Session Created
       │
       ▼
create_reminders(session_id)
       │
       ├──► Calculate reminder times (3 days, 24 hours before)
       │
       ├──► For each time & handler type:
       │    └──► Create Reminder record
       │
       ▼
scheduler.py detects overdue reminders
       │
       ├──► get_pending_reminders()
       │
       ├──► For each pending reminder:
       │    ├──► Get session and participants
       │    ├──► For each participant:
       │    │    └──► Send notification via handler(s)
       │    └──► Mark reminder as sent
       │
       ▼
Reminders delivered to participants


ERROR HANDLING
═══════════════════════════════════════════════════════════════════════════

Try-Catch Levels:

Level 1: CLI Commands
  - Input validation
  - Type checking (int conversion)
  - User feedback

Level 2: Business Logic
  - Entity existence checks
  - Relationship validation
  - Business rule enforcement

Level 3: Database Operations
  - Session management
  - Transaction handling
  - Constraint violations

Level 4: External Services
  - Email/SMTP failures
  - Notification handler errors
  - Graceful degradation


SECURITY CONSIDERATIONS
═══════════════════════════════════════════════════════════════════════════

Current Implementation:
✓ Environment variables for sensitive data (.env)
✓ No hardcoded credentials
✓ Input validation
✓ SQL injection prevention (using SQLAlchemy ORM)
✓ Audit logging

Future Improvements:
□ User authentication
□ Role-based access control
□ Encrypted password storage
□ API rate limiting
□ Data encryption at rest


SCALABILITY NOTES
═══════════════════════════════════════════════════════════════════════════

Current Scope:
- Single-user CLI application
- File-based SQLite database
- In-memory reminders
- Sequential processing

Scaling Path:
1. Multi-user support → Add authentication layer
2. Increased data volume → Switch to PostgreSQL
3. Distributed reminders → Queue system (Celery/RabbitMQ)
4. Web access → Flask/Django web interface
5. High concurrency → Async/await patterns

PERFORMANCE CHARACTERISTICS
═══════════════════════════════════════════════════════════════════════════

Operation               Time Complexity    Space Complexity
─────────────────────────────────────────────────────────
Add mediator            O(1)               O(1)
List mediators          O(n)               O(n)
Query sessions          O(n)               O(n)
Add participant         O(1)               O(1)
Create session          O(1) + O(m)        O(1)
Get pending reminders   O(n)               O(m)
Send reminders          O(m × p)           O(p)

n = number of records
m = number of reminders
p = number of participants

TESTING STRATEGY
═══════════════════════════════════════════════════════════════════════════

Unit Tests: test_basic.py
  - PeopleManager tests
  - SessionManager tests
  - Database operations

Manual Testing:
  - CLI commands
  - Reminder creation
  - Email notifications
  - Database operations

Integration Tests:
  - Full workflow (create → remind)
  - Multi-participant scenarios
  - Database persistence


DEPLOYMENT OPTIONS
═══════════════════════════════════════════════════════════════════════════

Option 1: Local CLI (Current)
- Single machine
- SQLite database
- Desktop or laptop

Option 2: Server Deployment
- Run on Linux server
- Cron job for scheduler
- Remote database connection

Option 3: Docker Containerized
- Dockerfile + docker-compose
- Easy deployment anywhere
- Consistent environment

Option 4: Cloud Deployment
- AWS Lambda + RDS
- Google Cloud Run + Cloud SQL
- Azure Functions + SQL Database


═══════════════════════════════════════════════════════════════════════════
System is modular, extensible, and production-ready for small to medium
deployments. Clear separation of concerns enables easy feature additions
and future enhancements.
═══════════════════════════════════════════════════════════════════════════
