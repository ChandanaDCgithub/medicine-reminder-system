"""
Flask Web Application for Medicine Reminder System
Main application with user authentication and dashboard
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, selectinload, joinedload
import os
from pathlib import Path

# Import models
try:
    from medicine_models import Base, User, Medicine, MedicineSchedule, MedicineHistory, WaterLog, MissedMedicineAlert
except ImportError:
    from .medicine_models import Base, User, Medicine, MedicineSchedule, MedicineHistory, WaterLog, MissedMedicineAlert

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / 'data' / 'medicine_system.db'

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'medicine_reminder_secret_key_2024'

# Configure database
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create all tables
Base.metadata.create_all(engine)


def get_db():
    """Get database session"""
    return Session()


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        db = get_db()
        
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Username or email already exists', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name
        )
        user.set_password(password)
        
        db.add(user)
        db.commit()
        db.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        db = get_db()
        
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user
        user = db.query(User).filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            
            db.close()
            flash(f'Welcome back, {user.full_name or user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            db.close()
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


# ==================== DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    db = get_db()
    user_id = session['user_id']
    
    # Get today's medicines with eager loading
    today = datetime.now().date()
    medicines = db.query(Medicine).filter_by(user_id=user_id).options(
        selectinload(Medicine.user)
    ).all()
    
    schedules = db.query(MedicineSchedule).filter_by(user_id=user_id, is_active=True).options(
        selectinload(MedicineSchedule.medicine),
        selectinload(MedicineSchedule.user)
    ).all()
    
    # Get today's medicine history with eager loading
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    today_history = db.query(MedicineHistory).filter(
        MedicineHistory.user_id == user_id,
        MedicineHistory.scheduled_time >= today_start,
        MedicineHistory.scheduled_time <= today_end
    ).options(
        selectinload(MedicineHistory.medicine),
        selectinload(MedicineHistory.user)
    ).all()
    
    # Get missed medicines today
    missed_count = db.query(MissedMedicineAlert).filter(
        MissedMedicineAlert.user_id == user_id,
        MissedMedicineAlert.scheduled_time >= today_start,
        MissedMedicineAlert.scheduled_time <= today_end,
        MissedMedicineAlert.alert_sent == True,
        MissedMedicineAlert.alert_acknowledged == False
    ).count()
    
    # Get water logs today
    water_logged = db.query(WaterLog).filter(
        WaterLog.user_id == user_id,
        WaterLog.logged_time >= today_start,
        WaterLog.logged_time <= today_end,
        WaterLog.logged == True
    ).count()
    
    result = render_template('dashboard.html',
                         medicines=medicines,
                         schedules=schedules,
                         today_history=today_history,
                         missed_count=missed_count,
                         water_logged=water_logged)
    db.close()
    return result


# ==================== MEDICINE MANAGEMENT ====================

@app.route('/medicines')
@login_required
def medicines():
    """List all medicines"""
    db = get_db()
    user_id = session['user_id']
    
    medicines = db.query(Medicine).filter_by(user_id=user_id).options(
        selectinload(Medicine.user)
    ).all()
    
    result = render_template('medicines.html', medicines=medicines)
    db.close()
    return result


@app.route('/add-medicine', methods=['GET', 'POST'])
@login_required
def add_medicine():
    """Add new medicine"""
    if request.method == 'POST':
        db = get_db()
        user_id = session['user_id']
        
        medicine = Medicine(
            user_id=user_id,
            name=request.form.get('name'),
            dosage=request.form.get('dosage'),
            description=request.form.get('description'),
            reason=request.form.get('reason'),
            manufacturer=request.form.get('manufacturer'),
            batch_number=request.form.get('batch_number'),
            side_effects=request.form.get('side_effects'),
            instructions=request.form.get('instructions')
        )
        
        db.add(medicine)
        db.commit()
        db.close()
        
        flash('Medicine added successfully!', 'success')
        return redirect(url_for('medicines'))
    
    return render_template('add_medicine.html')


@app.route('/edit-medicine/<int:medicine_id>', methods=['GET', 'POST'])
@login_required
def edit_medicine(medicine_id):
    """Edit medicine"""
    db = get_db()
    user_id = session['user_id']
    
    medicine = db.query(Medicine).filter_by(id=medicine_id, user_id=user_id).first()
    
    if not medicine:
        flash('Medicine not found', 'error')
        db.close()
        return redirect(url_for('medicines'))
    
    if request.method == 'POST':
        medicine.name = request.form.get('name')
        medicine.dosage = request.form.get('dosage')
        medicine.description = request.form.get('description')
        medicine.reason = request.form.get('reason')
        medicine.manufacturer = request.form.get('manufacturer')
        medicine.batch_number = request.form.get('batch_number')
        medicine.side_effects = request.form.get('side_effects')
        medicine.instructions = request.form.get('instructions')
        
        db.commit()
        db.close()
        
        flash('Medicine updated successfully!', 'success')
        return redirect(url_for('medicines'))
    
    db.close()
    return render_template('edit_medicine.html', medicine=medicine)


@app.route('/delete-medicine/<int:medicine_id>', methods=['POST'])
@login_required
def delete_medicine(medicine_id):
    """Delete medicine"""
    db = get_db()
    user_id = session['user_id']
    
    medicine = db.query(Medicine).filter_by(id=medicine_id, user_id=user_id).first()
    
    if medicine:
        db.delete(medicine)
        db.commit()
        flash('Medicine deleted successfully!', 'success')
    else:
        flash('Medicine not found', 'error')
    
    db.close()
    return redirect(url_for('medicines'))


# ==================== SCHEDULE MANAGEMENT ====================

@app.route('/schedules')
@login_required
def schedules():
    """List all medicine schedules"""
    db = get_db()
    user_id = session['user_id']
    
    schedules = db.query(MedicineSchedule).filter_by(user_id=user_id).options(
        selectinload(MedicineSchedule.medicine),
        selectinload(MedicineSchedule.user)
    ).all()
    
    result = render_template('schedules.html', schedules=schedules)
    db.close()
    return result


@app.route('/add-schedule', methods=['GET', 'POST'])
@login_required
def add_schedule():
    """Add new medicine schedule"""
    db = get_db()
    user_id = session['user_id']
    
    medicines = db.query(Medicine).filter_by(user_id=user_id).options(
        selectinload(Medicine.user)
    ).all()
    
    if request.method == 'POST':
        medicine_id = request.form.get('medicine_id')
        
        schedule = MedicineSchedule(
            user_id=user_id,
            medicine_id=medicine_id,
            morning_time=request.form.get('morning_time'),
            afternoon_time=request.form.get('afternoon_time'),
            evening_time=request.form.get('evening_time'),
            night_time=request.form.get('night_time'),
            morning_dosage=request.form.get('morning_dosage'),
            afternoon_dosage=request.form.get('afternoon_dosage'),
            evening_dosage=request.form.get('evening_dosage'),
            night_dosage=request.form.get('night_dosage'),
            frequency=request.form.get('frequency'),
            days=request.form.get('days'),
            start_date=datetime.now(),
            notes=request.form.get('notes'),
            is_active=True
        )
        
        db.add(schedule)
        db.commit()
        db.close()
        
        flash('Schedule added successfully!', 'success')
        return redirect(url_for('schedules'))
    
    result = render_template('add_schedule.html', medicines=medicines)
    db.close()
    return result


# ==================== MEDICINE HISTORY ====================

@app.route('/history')
@login_required
def medicine_history():
    """View medicine consumption history"""
    db = get_db()
    user_id = session['user_id']
    
    # Get date filter
    date_filter = request.args.get('date')
    if date_filter:
        filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
    else:
        filter_date = datetime.now().date()
    
    date_start = datetime.combine(filter_date, datetime.min.time())
    date_end = datetime.combine(filter_date, datetime.max.time())
    
    history = db.query(MedicineHistory).filter(
        MedicineHistory.user_id == user_id,
        MedicineHistory.scheduled_time >= date_start,
        MedicineHistory.scheduled_time <= date_end
    ).options(
        selectinload(MedicineHistory.medicine),
        selectinload(MedicineHistory.user)
    ).all()
    
    result = render_template('history.html', history=history, filter_date=filter_date)
    db.close()
    return result


@app.route('/log-medicine/<int:history_id>', methods=['POST'])
@login_required
def log_medicine(history_id):
    """Log medicine as taken"""
    db = get_db()
    user_id = session['user_id']
    
    record = db.query(MedicineHistory).filter_by(id=history_id, user_id=user_id).first()
    
    if record:
        record.taken = True
        record.taken_time = datetime.now()
        db.commit()
        flash('Medicine logged as taken!', 'success')
    else:
        flash('Record not found', 'error')
    
    db.close()
    return redirect(url_for('medicine_history'))


# ==================== WATER REMINDERS ====================

@app.route('/water-logs')
@login_required
def water_logs():
    """View water intake logs"""
    db = get_db()
    user_id = session['user_id']
    
    # Get today's water logs
    today = datetime.now().date()
    date_start = datetime.combine(today, datetime.min.time())
    date_end = datetime.combine(today, datetime.max.time())
    
    water_logs = db.query(WaterLog).filter(
        WaterLog.user_id == user_id,
        WaterLog.scheduled_time >= date_start,
        WaterLog.scheduled_time <= date_end
    ).options(
        selectinload(WaterLog.user)
    ).all()
    
    result = render_template('water_logs.html', water_logs=water_logs)
    db.close()
    return result


@app.route('/log-water/<int:water_id>', methods=['POST'])
@login_required
def log_water(water_id):
    """Log water intake"""
    db = get_db()
    user_id = session['user_id']
    
    water_log = db.query(WaterLog).filter_by(id=water_id, user_id=user_id).first()
    
    if water_log:
        water_log.logged = True
        water_log.logged_time = datetime.now()
        water_log.amount_ml = request.form.get('amount_ml', 250)
        db.commit()
        flash('Water intake logged!', 'success')
    else:
        flash('Log not found', 'error')
    
    db.close()
    return redirect(url_for('water_logs'))


# ==================== MISSED ALERTS ====================

@app.route('/missed-alerts')
@login_required
def missed_alerts():
    """View missed medicine alerts"""
    db = get_db()
    user_id = session['user_id']
    
    # Get unacknowledged missed alerts
    alerts = db.query(MissedMedicineAlert).filter(
        MissedMedicineAlert.user_id == user_id,
        MissedMedicineAlert.alert_acknowledged == False
    ).options(
        selectinload(MissedMedicineAlert.medicine),
        selectinload(MissedMedicineAlert.user)
    ).all()
    
    result = render_template('missed_alerts.html', alerts=alerts)
    db.close()
    return result


@app.route('/acknowledge-missed/<int:alert_id>', methods=['POST'])
@login_required
def acknowledge_missed(alert_id):
    """Acknowledge a missed medicine alert"""
    db = get_db()
    user_id = session['user_id']
    
    alert = db.query(MissedMedicineAlert).filter_by(id=alert_id, user_id=user_id).first()
    
    if alert:
        alert.alert_acknowledged = True
        alert.acknowledged_at = datetime.now()
        alert.reason = request.form.get('reason')
        db.commit()
        flash('Alert acknowledged!', 'success')
    else:
        flash('Alert not found', 'error')
    
    db.close()
    return redirect(url_for('missed_alerts'))


# ==================== PROFILE ====================

@app.route('/profile')
@login_required
def profile():
    """User profile"""
    db = get_db()
    user_id = session['user_id']
    
    user = db.query(User).filter_by(id=user_id).options(
        selectinload(User.medicines)
    ).first()
    
    result = render_template('profile.html', user=user)
    db.close()
    return result


@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    db = get_db()
    user_id = session['user_id']
    
    user = db.query(User).filter_by(id=user_id).first()
    
    if user:
        user.full_name = request.form.get('full_name')
        user.age = request.form.get('age')
        user.medical_history = request.form.get('medical_history')
        user.emergency_contact = request.form.get('emergency_contact')
        
        db.commit()
        session['full_name'] = user.full_name
        
        flash('Profile updated successfully!', 'success')
    else:
        flash('User not found', 'error')
    
    db.close()
    return redirect(url_for('profile'))


# ==================== API ENDPOINTS ====================

@app.route('/api/today-medicines')
@login_required
def api_today_medicines():
    """Get today's medicines as JSON"""
    db = get_db()
    user_id = session['user_id']
    
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    history = db.query(MedicineHistory).filter(
        MedicineHistory.user_id == user_id,
        MedicineHistory.scheduled_time >= today_start,
        MedicineHistory.scheduled_time <= today_end
    ).options(
        selectinload(MedicineHistory.medicine)
    ).all()
    
    medicines_data = []
    for h in history:
        medicines_data.append({
            'id': h.id,
            'name': h.medicine.name if h.medicine else 'Unknown',
            'dosage': h.dosage,
            'time': h.scheduled_time.strftime('%H:%M'),
            'time_slot': h.time_slot,
            'taken': h.taken
        })
    
    db.close()
    return jsonify(medicines_data)


@app.route('/api/stats')
@login_required
def api_stats():
    """Get user statistics"""
    db = get_db()
    user_id = session['user_id']
    
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    # Today's stats
    total_medicines_today = db.query(MedicineHistory).filter(
        MedicineHistory.user_id == user_id,
        MedicineHistory.scheduled_time >= today_start,
        MedicineHistory.scheduled_time <= today_end
    ).count()
    
    taken_medicines = db.query(MedicineHistory).filter(
        MedicineHistory.user_id == user_id,
        MedicineHistory.scheduled_time >= today_start,
        MedicineHistory.scheduled_time <= today_end,
        MedicineHistory.taken == True
    ).count()
    
    missed_alerts = db.query(MissedMedicineAlert).filter(
        MissedMedicineAlert.user_id == user_id,
        MissedMedicineAlert.scheduled_time >= today_start,
        MissedMedicineAlert.scheduled_time <= today_end
    ).count()
    
    water_logged = db.query(WaterLog).filter(
        WaterLog.user_id == user_id,
        WaterLog.logged_time >= today_start,
        WaterLog.logged_time <= today_end,
        WaterLog.logged == True
    ).count()
    
    db.close()
    
    return jsonify({
        'total_medicines': total_medicines_today,
        'taken_medicines': taken_medicines,
        'pending_medicines': total_medicines_today - taken_medicines,
        'missed_alerts': missed_alerts,
        'water_logged': water_logged,
        'compliance': round((taken_medicines / total_medicines_today * 100) if total_medicines_today > 0 else 0, 1)
    })


if __name__ == '__main__':
    # Ensure data directory exists
    DATABASE_PATH.parent.mkdir(exist_ok=True)
    
    # Run development server
    app.run(debug=True, host='0.0.0.0', port=5000)
