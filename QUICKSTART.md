# Medicine Reminder System - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd "mediation remainder system"
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python src/app.py
```

### Step 3: Open in Browser
Visit: **http://localhost:5000**

---

## 📋 System Ready Features

✅ **Complete Backend**
- Flask web server with 25+ routes
- SQLAlchemy ORM with 6 database models
- User authentication with password hashing
- RESTful API endpoints

✅ **Complete Frontend**
- 11 HTML templates with responsive design
- 500+ lines of professional CSS
- 250+ lines of interactive JavaScript
- Mobile-friendly UI

✅ **All Core Features Implemented**
- User registration & login
- Medicine CRUD operations
- 4-slot medicine scheduling (morning/afternoon/evening/night)
- Medicine history tracking
- Water intake logging with progress visualization
- Missed medicine alerts
- User profile management
- Dashboard with real-time statistics

---

## 🎯 First Time Usage

### 1. Create an Account
- Click **Register** at login page
- Fill in: Full Name, Username, Email, Password
- Click **Create Account**

### 2. Add Your First Medicine
- Click **Medicines** → **Add Medicine**
- Fill in medicine details:
  - Name (e.g., "Aspirin")
  - Dosage (e.g., "500mg")
  - Reason (e.g., "Pain relief")
  - Other optional fields
- Click **Add Medicine**

### 3. Create a Schedule
- Click **Schedules** → **Add Schedule**
- Select your medicine
- Choose time slots (pick morning, afternoon, or both)
- Set frequency (daily, alternate, weekly)
- Click **Create Schedule**

### 4. Log Your Medicines
- Go to **Dashboard**
- Under "Today's Medicines", click **Mark as Taken**
- Track your compliance on the dashboard

### 5. Track Water Intake
- Click **Water Logs**
- Enter amount in milliliters
- Click **Log Water**
- Watch progress bar fill up!

---

## 📊 Dashboard Overview

The **Dashboard** shows:
- 📅 **Today's Medicines**: Count of scheduled medicines
- ✓ **Taken**: Medicines you've already logged
- ⏳ **Pending**: Medicines waiting to be taken
- ❌ **Missed**: Medicines that were skipped
- 💧 **Water Intake**: Daily water consumption progress
- 📈 **Compliance**: Your medicine adherence percentage

---

## 🧭 Navigation Guide

### Main Menu (Top Navigation)
- **Dashboard** - Home page with statistics
- **Medicines** - View, add, edit medicines
- **Schedules** - Create time-based schedules
- **History** - View all logged medicines
- **Water Logs** - Track water intake
- **Missed Alerts** - Review skipped doses
- **Profile** - Your account settings
- **Logout** - Exit the system

### Dashboard Quick Actions
- **Add Medicine** - Create new medicine entry
- **Create Schedule** - Set up medicine times
- **View History** - Check past logs
- **Track Water** - Log water intake
- **My Profile** - Update personal info

---

## 💡 Useful Tips

### Time Slots
- **Morning**: 6 AM - 12 PM
- **Afternoon**: 12 PM - 5 PM  
- **Evening**: 5 PM - 9 PM
- **Night**: 9 PM - 12 AM

### Set Multiple Times
You can set the same medicine for multiple time slots in one schedule. For example:
- Morning at 8 AM (500mg)
- Evening at 8 PM (250mg)

### Water Intake Goal
Track your daily water consumption toward a healthy goal. Common recommendations are 2-3 liters (2000-3000 ml) per day.

### Missed Alerts
When you skip a medicine:
1. An alert is automatically created
2. Go to **Missed Alerts** 
3. Click **Acknowledge** and optionally explain why
4. This helps track patterns

### Medicine History
View complete history of when you took medicines. Useful for:
- Checking if you took your medicine
- Searching by date
- Printing or exporting

---

## 🔧 Technical Details

### Database
- **Location**: `data/medicine_system.db`
- **Type**: SQLite
- **Auto-created**: First time you run

### Directories Created
```
src/
├── medicine_models.py      (Database models)
├── app.py                  (Flask application)
├── templates/              (HTML files)
└── static/
    ├── css/style.css       (Styling)
    └── js/script.js        (Interactivity)
```

### Port
- Default: `5000`
- If in use, change in `app.py`: `app.run(debug=True, port=5001)`

---

## ⚙️ System Requirements

- Python 3.8+
- Flask 3.0+
- SQLAlchemy 2.1+
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Edit `app.py`, change port to 5001 |
| Database not found | Delete `data/medicine_system.db`, restart (will auto-create) |
| Can't login | Check username/password. Confirm account was registered |
| Missing CSS/JS | Ensure `src/static/css/style.css` and `src/static/js/script.js` exist |
| Python import errors | Run `pip install -r requirements.txt` again |

---

## 📚 Full Documentation

For detailed information, see **README.md**

---

## ✨ What's Next?

The system is fully functional with all requested features:
- ✅ User login & registration
- ✅ Add/edit medicines
- ✅ Create schedules with 4 time slots
- ✅ Water remainder tracking
- ✅ Missed medicine alerts
- ✅ Medicine history
- ✅ Dashboard with statistics
- ✅ Responsive web UI

### Optional Enhancements (Future)
- Email/SMS notifications
- Push notifications
- Mobile app
- Export to PDF/Excel
- Dark mode
- Data backup

---

**Enjoy using your Medicine Reminder System! Stay healthy! 💚**
