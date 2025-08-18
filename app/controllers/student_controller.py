from flask import render_template, session, redirect, url_for, flash
from app.models.book import Book


class StudentController:
    @staticmethod
    def student_dashboard():
        if 'user_id' not in session or session.get('user_role') != 'Student':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        user_reservation_count = Book.get_user_reservation_count(user_id)
        
        dummy_stats = {
            'issued_books': 3,
            'available_books': 1247,
            'pending_fines': 0,
            'reservations': user_reservation_count
        }
        
        dummy_notifications = [
            {'message': 'Book "Python Programming" is due in 2 days', 'time': '2 hours ago'},
            {'message': 'Your reservation for "Data Structures" is ready', 'time': '1 day ago'},
            {'message': 'Fine of $15.50 has been added to your account', 'time': '3 days ago'}
        ]
        
        return render_template('dashboard/student_dashboard.html', 
                             user_name=session.get('user_name'),
                             stats=dummy_stats,
                             notifications=dummy_notifications)
