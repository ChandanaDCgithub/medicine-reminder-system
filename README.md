# Medicine Reminder System

A comprehensive web-based medicine reminder application built with Python Flask. This system helps users manage their medications with scheduled reminders, water intake tracking, missed medicine alerts, and comprehensive history tracking.

## Features

### 🔐 User Authentication
- User registration with email validation
- Secure login with password hashing
- User profile management
- Personal medical history tracking

### 💊 Medicine Management
- Add, edit, and delete medicines
- Store detailed medicine information (dosage, manufacturer, expiry date, etc.)
- View complete medicine list with details
- Track side effects and instructions

### ⏰ Scheduling System
- Create medicine schedules with 4 time slots:
  - **Morning** (6:00 AM - 12:00 PM)
  - **Afternoon** (12:00 PM - 5:00 PM)
  - **Evening** (5:00 PM - 9:00 PM)
  - **Night** (9:00 PM - 12:00 AM)
- Set custom dosages for each time slot
- Define frequency (daily, alternate days, weekly, etc.)
- Date range specification

### 📋 Medicine History
- Log medicine consumption with timestamps
- View complete history with filters
- Mark medicines as taken
- Track pending doses

### 💧 Water Intake Tracking
- Log water intake with amount in ml
- Daily water intake visualization
- Progress tracking towards daily goals
- Scheduled water reminders

### 🚨 Missed Medicine Alerts
- Automatic alerts for missed doses
- Reason tracking for missed medicines
- Alert acknowledgement system
- History of missed medicines

### 📊 Dashboard & Analytics
- Real-time statistics:
  - Today's medicines count
  - Medicines taken today
  - Pending medicines
  - Missed medicines
  - Water intake progress
  - Medicine compliance percentage
- Quick action cards for common tasks
- Today's medicines at a glance

## Tech Stack

- **Backend**: Python 3.14 with Flask 3.0+
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Werkzeug password hashing
- **API**: RESTful JSON endpoints

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. Clone or navigate to the project directory:
```bash
cd "mediation remainder system"
```

2. Create a virtual environment (optional but recommended):
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create necessary directories:
```bash
mkdir -p data
```
## Running the Application

### Start the Flask Development Server

```bash
# Navigate to the project directory
cd "mediation remainder system"

# Activate virtual environment (if created)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run the application
python src/app.py
```

The application will start on `http://localhost:5000`

### Default Access
- Open your browser and go to: `http://localhost:5000`
- You'll be redirected to the login page
- Create a new account or use test credentials

## Project Structure

```
mediation remainder system/
├── src/
│   ├── app.py                    # Flask application with all routes
│   ├── medicine_models.py        # SQLAlchemy database models
│   ├── templates/                # HTML templates
│   │   ├── base.html             # Base template with navigation
│   │   ├── login.html            # Login page
│   │   ├── register.html         # Registration page
│   │   ├── dashboard.html        # Main dashboard
│   │   ├── medicines.html        # Medicine list
│   │   ├── add_medicine.html     # Add medicine form
│   │   ├── edit_medicine.html    # Edit medicine form
│   │   ├── schedules.html        # Medicine schedules
│   │   ├── add_schedule.html     # Add schedule form
│   │   ├── history.html          # Medicine history
│   │   ├── water_logs.html       # Water intake tracker
│   │   ├── missed_alerts.html    # Missed medicine alerts
│   │   └── profile.html          # User profile
│   └── static/
│       ├── css/
│       │   └── style.css         # Main stylesheet (500+ lines)
│       └── js/
│           └── script.js         # JavaScript functionality
├── data/
│   └── medicine_system.db        # SQLite database (auto-created)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── main.py                       # Optional entry point (uses app.py)
```

## Database Models

### User
- Stores user account information
- Encrypted password storage
- Personal profile data

### Medicine
- Medicine details (name, dosage, manufacturer, etc.)
- Expiry dates and batch information
- Side effects and usage instructions

### MedicineSchedule
- Scheduling information for medicines
- 4 time slots with individual dosages
- Frequency and date range

### MedicineHistory
- Records of taken/pending medicines
- Scheduled vs actual consumption times
- Consumption status tracking

### WaterLog
- Water intake records
- Amount in milliliters
- Timestamp tracking

### MissedMedicineAlert
- Alert records for missed doses
- Reason tracking
- Acknowledgement status

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Dashboard & Statistics
- `GET /dashboard` - Main dashboard
- `GET /api/stats` - Dashboard statistics (JSON)
- `GET /api/today-medicines` - Today's medicines (JSON)

### Medicine Management
- `GET /medicines` - List all medicines
- `POST /add-medicine` - Add new medicine
- `POST /edit-medicine/<id>` - Edit medicine
- `POST /delete-medicine/<id>` - Delete medicine

### Scheduling
- `GET /schedules` - View schedules
- `POST /add-schedule` - Create schedule

### Medicine Logging
- `GET /history` - Medicine history
- `POST /log-medicine` - Log medicine consumption

### Water Tracking
- `GET /water-logs` - Water intake log
- `POST /log-water` - Log water intake

### Alerts
- `GET /missed-alerts` - View missed alerts
- `POST /acknowledge-missed/<id>` - Acknowledge alert

### User Profile
- `GET /profile` - User profile page
- `POST /update-profile` - Update profile

## Usage Guide

### 1. Registration
1. Open the application
2. Click "Register" on the login page
3. Fill in your details:
   - Full Name
   - Username
   - Email
   - Password (minimum 6 characters)
4. Click "Create Account"

### 2. Adding a Medicine
1. Go to **Medicines** → **Add Medicine**
2. Enter medicine details:
   - Name
   - Dosage
   - Reason for use
   - Manufacturer
   - Batch number
   - Expiry date
   - Side effects
   - Usage instructions
3. Click "Add Medicine"

### 3. Creating a Schedule
1. Go to **Schedules** → **Add Schedule**
2. Select the medicine
3. Choose time slots (morning, afternoon, evening, night)
4. Set frequency
5. Specify date range
6. Click "Create Schedule"

### 4. Logging Medicine
1. Go to **Dashboard**
2. Find medicine in "Today's Medicines"
3. Click "Mark as Taken"
4. Confirm the action

### 5. Tracking Water Intake
1. Go to **Water Logs**
2. Enter amount in milliliters
3. Click "Log Water"
4. View progress bar with daily intake

### 6. Viewing History
1. Go to **History**
2. View all logged medicines
3. Filter by date if needed
4. See pending and completed doses

### 7. Managing Missed Alerts
1. Go to **Missed Alerts**
2. Review missed medicines
3. Click "Acknowledge" to mark as reviewed
4. Optionally provide a reason

### 8. User Profile
1. Go to **Profile**
2. Update personal information
3. Add medical history
4. View statistics and emergency contacts

## Features in Detail

### Medicine Compliance Tracking
- Dashboard shows daily compliance percentage
- Based on scheduled vs completed medicines
- Helps monitor medication adherence

### Missed Medicine Notifications
- Automatic alerts for overdue medicines
- Can be acknowledged with reasons
- Historical tracking of missed doses

### Time-Based Scheduling
- Four configurable time slots per day
- Individual dosage per time slot
- Flexible frequency options

### Water Intake Program
- Integrated water reminder system
- Visual progress tracking
- Daily intake logging

## Troubleshooting

### Database Not Found
- Ensure the `data/` directory exists
- Database is auto-created on first run

### Port Already in Use
If port 5000 is in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to different port
```

### Login Issues
- Verify username and password
- Ensure user is registered
- Check if database has been initialized

### Missing Static Files
- Ensure `src/static/css/` and `src/static/js/` directories exist
- Verify `style.css` and `script.js` are present

## Security Notes

- Passwords are hashed using Werkzeug's safe_str_cmp
- Session-based authentication
- User data is isolated per user
- Database uses SQLite (suitable for personal/small group use)

## Future Enhancements

- Email/SMS notifications for reminders
- Mobile app version
- Multi-device synchronization
- Advanced analytics and reporting
- Push notifications
- Medication refill tracking
- Doctor integration
- Pharmacy integration
- Export reports (PDF, CSV)
- Dark mode

## Support & Contributing

For issues or suggestions, please contact the development team or check the application logs.

## License

This project is provided as-is for personal and educational use.

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: Production Ready
