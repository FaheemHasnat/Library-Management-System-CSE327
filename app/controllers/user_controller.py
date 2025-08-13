<<<<<<< HEAD
=======
"""
User Controller for Library Management System
Handles authentication routes (login, signup, logout)
"""

>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user_model import UserModel
import logging

<<<<<<< HEAD
=======
# Create blueprint for user routes
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
<<<<<<< HEAD
=======
    """
    Handle user login
    GET: Display login form
    POST: Process login credentials
    """
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            
<<<<<<< HEAD
=======
            # Validate input
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
            if not email or not password:
                flash('Please fill in all fields', 'error')
                return render_template('login.html')
            
<<<<<<< HEAD
            user = UserModel.authenticate_user(email, password)
            
            if user:
=======
            # Authenticate user
            user = UserModel.authenticate_user(email, password)
            
            if user:
                # Store user information in session
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
                session['user_id'] = user['UserID']
                session['user_name'] = user['Name']
                session['user_email'] = user['Email']
                session['user_role'] = user['Role']
                session['logged_in'] = True
                
                flash(f'Welcome back, {user["Name"]}!', 'success')
                
<<<<<<< HEAD
=======
                # Redirect based on role
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
                if user['Role'] == 'Admin':
                    return redirect(url_for('dashboard.admin_dashboard'))
                elif user['Role'] == 'Librarian':
                    return redirect(url_for('dashboard.librarian_dashboard'))
<<<<<<< HEAD
                else:
=======
                else:  # Student
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
                    return redirect(url_for('dashboard.student_dashboard'))
            else:
                flash('Invalid email or password', 'error')
                
        except Exception as e:
            logging.error(f"Login error: {e}")
            flash('Login failed due to system error', 'error')
    
    return render_template('login.html')


@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
<<<<<<< HEAD
=======
    """
    Handle user registration
    GET: Display signup form
    POST: Process registration data
    """
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            role = request.form.get('role', 'Student').strip()
            
<<<<<<< HEAD
=======
            # Validate input
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
            if not all([name, email, password, confirm_password]):
                flash('Please fill in all fields', 'error')
                return render_template('signup.html')
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('signup.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long', 'error')
                return render_template('signup.html')
            
<<<<<<< HEAD
            valid_roles = ['Student', 'Librarian', 'Admin']
            if role not in valid_roles:
                role = 'Student'
            
=======
            # Validate role
            valid_roles = ['Student', 'Librarian', 'Admin']
            if role not in valid_roles:
                role = 'Student'  # Default to Student
            
            # Register user
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
            result = UserModel.register_user(name, email, password, role)
            
            if result['success']:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('user.login'))
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            logging.error(f"Signup error: {e}")
            flash('Registration failed due to system error', 'error')
    
    return render_template('signup.html')


@user_bp.route('/logout')
def logout():
<<<<<<< HEAD
    try:
=======
    """Handle user logout"""
    try:
        # Clear session data
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
        session.clear()
        flash('You have been logged out successfully', 'info')
        
    except Exception as e:
        logging.error(f"Logout error: {e}")
        flash('Logout error occurred', 'error')
    
    return redirect(url_for('user.login'))


@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
<<<<<<< HEAD
=======
    """
    Handle user profile management
    GET: Display profile form
    POST: Update profile information
    """
    # Check if user is logged in
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
    if not session.get('logged_in'):
        flash('Please login to access your profile', 'error')
        return redirect(url_for('user.login'))
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            
<<<<<<< HEAD
=======
            # Validate input
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
            if not name or not email:
                flash('Please fill in all fields', 'error')
                return render_template('user_profile.html', user=session)
            
<<<<<<< HEAD
=======
            # Update profile
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
            result = UserModel.update_user_profile(
                session['user_id'], 
                name, 
                email
            )
            
            if result['success']:
<<<<<<< HEAD
=======
                # Update session data
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
                session['user_name'] = name
                session['user_email'] = email
                flash('Profile updated successfully', 'success')
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            logging.error(f"Profile update error: {e}")
            flash('Profile update failed due to system error', 'error')
    
    return render_template('user_profile.html', user=session)


@user_bp.route('/change-password', methods=['POST'])
def change_password():
<<<<<<< HEAD
=======
    """Handle password change"""
    # Check if user is logged in
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
    if not session.get('logged_in'):
        flash('Please login to change your password', 'error')
        return redirect(url_for('user.login'))
    
    try:
        old_password = request.form.get('old_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
<<<<<<< HEAD
=======
        # Validate input
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
        if not all([old_password, new_password, confirm_password]):
            flash('Please fill in all password fields', 'error')
            return redirect(url_for('user.profile'))
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('user.profile'))
        
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long', 'error')
            return redirect(url_for('user.profile'))
        
<<<<<<< HEAD
=======
        # Change password
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
        result = UserModel.change_password(
            session['user_id'], 
            old_password, 
            new_password
        )
        
        if result['success']:
            flash('Password changed successfully', 'success')
        else:
            flash(result['message'], 'error')
            
    except Exception as e:
        logging.error(f"Password change error: {e}")
        flash('Password change failed due to system error', 'error')
    
    return redirect(url_for('user.profile'))


def login_required(f):
<<<<<<< HEAD
=======
    """
    Decorator to require login for certain routes
    
    Args:
        f: Function to decorate
    
    Returns:
        Decorated function
    """
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please login to access this page', 'error')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    
    return decorated_function


def role_required(required_roles):
<<<<<<< HEAD
=======
    """
    Decorator to require specific roles for certain routes
    
    Args:
        required_roles (list): List of allowed roles
    
    Returns:
        Decorator function
    """
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
    from functools import wraps
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                flash('Please login to access this page', 'error')
                return redirect(url_for('user.login'))
            
            user_role = session.get('user_role')
            if user_role not in required_roles:
                flash('You do not have permission to access this page', 'error')
                return redirect(url_for('dashboard.student_dashboard'))
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator
