from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from models import db, Event, Guest, Booking, User
from config import Config
from datetime import datetime
from sqlalchemy import func
from functools import wraps
import re
import random

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()


# Validation helper functions
def validate_gmail(email):
    """Validate that email is a Gmail address"""
    if not email:
        return True  # Allow empty email
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate that phone is exactly 10 digits"""
    if not phone:
        return True  # Allow empty phone
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone) is not None

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============= AUTHENTICATION ROUTES =============

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username/email or password', 'error')
    
    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            full_name = request.form.get('full_name')
            
            # Validate passwords match
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('auth/register.html')
            
            # Validate Gmail only
            if not email.lower().endswith('@gmail.com'):
                flash('Invalid email! Only @gmail.com addresses are allowed.', 'error')
                return render_template('auth/register.html')
            
            # Check if username exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
                return render_template('auth/register.html')
            
            # Check if email exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return render_template('auth/register.html')
            
            # Create new user
            user = User(
                username=username,
                email=email,
                full_name=full_name
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('auth/register.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))


# Dashboard Route
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing overview of all events"""
    total_events = Event.query.count()
    upcoming_events = Event.query.filter(Event.event_date >= datetime.now().date()).count()
    total_guests = Guest.query.count()
    total_bookings = Booking.query.count()
    
    # Get recent events
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(5).all()
    
    # Calculate total budget
    total_budget = db.session.query(func.sum(Event.budget)).scalar() or 0
    
    # RSVP statistics
    rsvp_stats = {
        'accepted': Guest.query.filter_by(rsvp_status='Accepted').count(),
        'pending': Guest.query.filter_by(rsvp_status='Pending').count(),
        'declined': Guest.query.filter_by(rsvp_status='Declined').count()
    }
    
    return render_template('dashboard.html', 
                         total_events=total_events,
                         upcoming_events=upcoming_events,
                         total_guests=total_guests,
                         total_bookings=total_bookings,
                         recent_events=recent_events,
                         total_budget=total_budget,
                         rsvp_stats=rsvp_stats)


# ============= EVENT ROUTES =============

@app.route('/events')
def events_list():
    """List all events"""
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('events/list.html', events=events)


@app.route('/events/create', methods=['GET', 'POST'])
def event_create():
    """Create a new event"""
    if request.method == 'POST':
        try:
            event = Event(
                name=request.form['name'],
                description=request.form.get('description'),
                event_date=datetime.strptime(request.form['event_date'], '%Y-%m-%d').date(),
                event_time=datetime.strptime(request.form['event_time'], '%H:%M').time() if request.form.get('event_time') else None,
                location=request.form.get('location'),
                latitude=float(request.form.get('latitude')) if request.form.get('latitude') else None,
                longitude=float(request.form.get('longitude')) if request.form.get('longitude') else None,
                venue_capacity=int(request.form.get('venue_capacity')) if request.form.get('venue_capacity') else None,
                budget=float(request.form.get('budget', 0)),
                status=request.form.get('status', 'Planning')
            )
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('events_list'))
        except Exception as e:
            flash(f'Error creating event: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('events/create.html')


@app.route('/events/<int:id>')
def event_detail(id):
    """View event details"""
    event = Event.query.get_or_404(id)
    guests = Guest.query.filter_by(event_id=id).all()
    bookings = Booking.query.filter_by(event_id=id).all()
    
    # Calculate total booking cost
    total_booking_cost = sum([float(b.cost) for b in bookings])
    
    return render_template('events/detail.html', 
                         event=event, 
                         guests=guests, 
                         bookings=bookings,
                         total_booking_cost=total_booking_cost)


@app.route('/events/<int:id>/edit', methods=['GET', 'POST'])
def event_edit(id):
    """Edit an event"""
    event = Event.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            event.name = request.form['name']
            event.description = request.form.get('description')
            event.event_date = datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()
            event.event_time = datetime.strptime(request.form['event_time'], '%H:%M').time() if request.form.get('event_time') else None
            event.location = request.form.get('location')
            event.latitude = float(request.form.get('latitude')) if request.form.get('latitude') else None
            event.longitude = float(request.form.get('longitude')) if request.form.get('longitude') else None
            event.venue_capacity = int(request.form.get('venue_capacity')) if request.form.get('venue_capacity') else None
            event.budget = float(request.form.get('budget', 0))
            event.status = request.form.get('status', 'Planning')
            
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('event_detail', id=id))
        except Exception as e:
            flash(f'Error updating event: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('events/edit.html', event=event)


@app.route('/events/<int:id>/delete', methods=['POST'])
def event_delete(id):
    """Delete an event"""
    try:
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting event: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('events_list'))


# ============= GUEST ROUTES =============

@app.route('/guests')
def guests_list():
    """List all guests"""
    guests = Guest.query.order_by(Guest.created_at.desc()).all()
    return render_template('guests/list.html', guests=guests)


@app.route('/guests/create', methods=['GET', 'POST'])
def guest_create():
    """Create a new guest"""
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            phone = request.form.get('phone')
            event_id = int(request.form['event_id'])
            guest_count = int(request.form.get('guest_count', 1))
            
            # Validate Gmail
            if email and not validate_gmail(email):
                flash('Error: Only Gmail addresses are accepted (e.g., user@gmail.com)', 'error')
                events = Event.query.all()
                return render_template('guests/create.html', events=events)
            
            # Validate Phone
            if phone and not validate_phone(phone):
                flash('Error: Phone number must be exactly 10 digits', 'error')
                events = Event.query.all()
                return render_template('guests/create.html', events=events)
            
            # Check venue capacity
            event = Event.query.get(event_id)
            if event and event.venue_capacity:
                current_guests = db.session.query(func.sum(Guest.guest_count)).filter_by(event_id=event_id).scalar() or 0
                if current_guests + guest_count > event.venue_capacity:
                    flash(f'Error: Adding {guest_count} guests would exceed venue capacity of {event.venue_capacity}. Current guests: {current_guests}', 'error')
                    events = Event.query.all()
                    return render_template('guests/create.html', events=events)
            
            guest = Guest(
                event_id=event_id,
                name=request.form['name'],
                email=email,
                phone=phone,
                rsvp_status=request.form.get('rsvp_status', 'Pending'),
                guest_count=guest_count,
                dietary_requirements=request.form.get('dietary_requirements')
            )
            db.session.add(guest)
            db.session.commit()
            flash('Guest added successfully!', 'success')
            return redirect(url_for('guests_list'))
        except Exception as e:
            flash(f'Error adding guest: {str(e)}', 'error')
            db.session.rollback()
    
    events = Event.query.all()
    return render_template('guests/create.html', events=events)


@app.route('/guests/<int:id>/edit', methods=['GET', 'POST'])
def guest_edit(id):
    """Edit a guest"""
    guest = Guest.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            phone = request.form.get('phone')
            
            # Validate Gmail
            if email and not validate_gmail(email):
                flash('Error: Only Gmail addresses are accepted (e.g., user@gmail.com)', 'error')
                events = Event.query.all()
                return render_template('guests/edit.html', guest=guest, events=events)
            
            # Validate Phone
            if phone and not validate_phone(phone):
                flash('Error: Phone number must be exactly 10 digits', 'error')
                events = Event.query.all()
                return render_template('guests/edit.html', guest=guest, events=events)
            
            guest.event_id = int(request.form['event_id'])
            guest.name = request.form['name']
            guest.email = email
            guest.phone = phone
            guest.rsvp_status = request.form.get('rsvp_status', 'Pending')
            guest.guest_count = int(request.form.get('guest_count', 1))
            guest.dietary_requirements = request.form.get('dietary_requirements')
            
            db.session.commit()
            flash('Guest updated successfully!', 'success')
            return redirect(url_for('guests_list'))
        except Exception as e:
            flash(f'Error updating guest: {str(e)}', 'error')
            db.session.rollback()
    
    events = Event.query.all()
    return render_template('guests/edit.html', guest=guest, events=events)


@app.route('/guests/<int:id>/delete', methods=['POST'])
def guest_delete(id):
    """Delete a guest"""
    try:
        guest = Guest.query.get_or_404(id)
        db.session.delete(guest)
        db.session.commit()
        flash('Guest deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting guest: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('guests_list'))


# ============= BOOKING ROUTES =============

@app.route('/bookings')
def bookings_list():
    """List all bookings"""
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('bookings/list.html', bookings=bookings)


@app.route('/bookings/create', methods=['GET', 'POST'])
def booking_create():
    """Create a new booking"""
    if request.method == 'POST':
        try:
            # Automatically set status to Confirmed instead of Pending
            booking = Booking(
                event_id=int(request.form['event_id']),
                booking_type=request.form['booking_type'],
                vendor_name=request.form['vendor_name'],
                description=request.form.get('description'),
                cost=float(request.form.get('cost', 0)),
                booking_date=datetime.strptime(request.form['booking_date'], '%Y-%m-%d').date() if request.form.get('booking_date') else None,
                status='Confirmed',  # Auto-confirm bookings
                contact_info=request.form.get('contact_info'),
                notes=request.form.get('notes')
            )
            db.session.add(booking)
            db.session.commit()
            flash('Booking created and automatically confirmed!', 'success')
            return redirect(url_for('bookings_list'))
        except Exception as e:
            flash(f'Error creating booking: {str(e)}', 'error')
            db.session.rollback()
    
    events = Event.query.all()
    return render_template('bookings/create.html', events=events)


@app.route('/bookings/<int:id>/edit', methods=['GET', 'POST'])
def booking_edit(id):
    """Edit a booking"""
    booking = Booking.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            booking.event_id = int(request.form['event_id'])
            booking.booking_type = request.form['booking_type']
            booking.vendor_name = request.form['vendor_name']
            booking.description = request.form.get('description')
            booking.cost = float(request.form.get('cost', 0))
            booking.booking_date = datetime.strptime(request.form['booking_date'], '%Y-%m-%d').date() if request.form.get('booking_date') else None
            booking.status = request.form.get('status', 'Pending')
            booking.contact_info = request.form.get('contact_info')
            booking.notes = request.form.get('notes')
            
            db.session.commit()
            flash('Booking updated successfully!', 'success')
            return redirect(url_for('bookings_list'))
        except Exception as e:
            flash(f'Error updating booking: {str(e)}', 'error')
            db.session.rollback()
    
    events = Event.query.all()
    return render_template('bookings/edit.html', booking=booking, events=events)


@app.route('/bookings/<int:id>/delete', methods=['POST'])
def booking_delete(id):
    """Delete a booking"""
    try:
        booking = Booking.query.get_or_404(id)
        db.session.delete(booking)
        db.session.commit()
        flash('Booking deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting booking: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('bookings_list'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
