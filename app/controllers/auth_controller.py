from flask import render_template, request, redirect, url_for, session, flash
from app.models.user import User

class AuthController:
    @staticmethod
    def librarian_dashboard():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        return render_template('dashboard/librarian_dashboard.html', user_name=session.get('user_name'))

    @staticmethod
    def student_dashboard():
        if 'user_id' not in session or session.get('user_role') != 'Student':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        return render_template('dashboard/student_dashboard.html', user_name=session.get('user_name'))
    @staticmethod
    def admin_book_status():
        if 'user_id' not in session or session.get('user_role') != 'Admin':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        User.initialize_sample_data()
        books = User.get_all_books()
        return render_template('admin/book_status.html', user_name=session.get('user_name'), books=books)

    @staticmethod
    def librarian_book_status():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        User.initialize_sample_data()
        books = User.get_all_books()
        return render_template('librarian/book_status.html', user_name=session.get('user_name'), books=books)

    @staticmethod
    def student_book_status():
        if 'user_id' not in session or session.get('user_role') != 'Student':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        User.initialize_sample_data()
        books = User.get_all_books()
        return render_template('student/book_status.html', user_name=session.get('user_name'), books=books)
    @staticmethod
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                flash('Please enter both email and password', 'error')
                return render_template('auth/login.html')
            
            User.initialize_sample_data()
            user = User.authenticate(email, password)
            
            if user:
                session['user_id'] = user.user_id
                session['user_name'] = user.name
                session['user_email'] = user.email
                session['user_role'] = user.role
                
                flash(f'Welcome back, {user.name}!', 'success')
                
                if user.role == 'Admin':
                    return redirect(url_for('admin_dashboard'))
                elif user.role == 'Librarian':
                    return redirect(url_for('librarian_dashboard'))
                elif user.role == 'Student':
                    return redirect(url_for('student_dashboard'))
                else:
                    return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'error')
                return render_template('auth/login.html')
        
        return render_template('auth/login.html')
    
    @staticmethod
    def signup():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            role = request.form.get('role')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if not all([name, email, role, password, confirm_password]):
                flash('Please fill in all fields', 'error')
                return render_template('auth/signup.html')
            
            if role not in ['Student', 'Librarian']:
                flash('Invalid role selected', 'error')
                return render_template('auth/signup.html')
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('auth/signup.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long', 'error')
                return render_template('auth/signup.html')
            
            if User.get_by_email(email):
                flash('Email already exists', 'error')
                return render_template('auth/signup.html')
            
            user = User.create_user(name, email, password, role)
            
            if user:
                flash('Account created successfully! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error creating account. Please try again.', 'error')
                return render_template('auth/signup.html')
        
        return render_template('auth/signup.html')
    
    @staticmethod
    def logout():
        session.clear()
        flash('You have been logged out successfully', 'success')
        return redirect(url_for('login'))
    
    @staticmethod
    def dashboard():
        if 'user_id' not in session:
            flash('Please log in to access the dashboard', 'error')
            return redirect(url_for('login'))
        
        user_role = session.get('user_role')
        user_name = session.get('user_name')
        
        return render_template('dashboard/dashboard.html', user_role=user_role, user_name=user_name)
    
    @staticmethod
    def admin_dashboard():
        if 'user_id' not in session or session.get('user_role') != 'Admin':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        return render_template('dashboard/admin_dashboard.html', user_name=session.get('user_name'))
