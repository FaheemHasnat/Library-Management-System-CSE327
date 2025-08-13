"""
Dashboard Controller for Library Management System
Handles role-based dashboard routes and data display
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from app.models.dashboard_model import DashboardModel
from app.controllers.user_controller import login_required, role_required
import logging

# Create blueprint for dashboard routes
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Route users to appropriate dashboard based on their role
    """
    user_role = session.get('user_role')
    
    if user_role == 'Admin':
        return redirect(url_for('dashboard.admin_dashboard'))
    elif user_role == 'Librarian':
        return redirect(url_for('dashboard.librarian_dashboard'))
    else:  # Student
        return redirect(url_for('dashboard.student_dashboard'))


@dashboard_bp.route('/admin')
@login_required
@role_required(['Admin'])
def admin_dashboard():
    """
    Admin dashboard with system-wide statistics and controls
    """
    try:
        # Get system statistics
        stats = DashboardModel.get_system_statistics()
        
        # Get recent notifications
        notifications = DashboardModel.get_recent_notifications(
            session['user_id'], 
            'Admin'
        )
        
        # Get overdue books details
        overdue_books = DashboardModel.get_overdue_books_details('Admin')
        
        # Get recent transactions
        recent_transactions = DashboardModel.get_recent_transactions('Admin')
        
        if stats is None:
            flash('Unable to load dashboard statistics', 'error')
            stats = {}
        
        return render_template(
            'dashboard_admin.html',
            user=session,
            stats=stats,
            notifications=notifications,
            overdue_books=overdue_books,
            recent_transactions=recent_transactions
        )
        
    except Exception as e:
        logging.error(f"Admin dashboard error: {e}")
        flash('Dashboard loading failed', 'error')
        return render_template('dashboard_admin.html', user=session, stats={})


@dashboard_bp.route('/librarian')
@login_required
@role_required(['Librarian', 'Admin'])
def librarian_dashboard():
    """
    Librarian dashboard with library operation statistics
    """
    try:
        # Get librarian-specific statistics
        stats = DashboardModel.get_librarian_statistics()
        
        # Get recent notifications
        notifications = DashboardModel.get_recent_notifications(
            session['user_id'], 
            'Librarian'
        )
        
        # Get overdue books details
        overdue_books = DashboardModel.get_overdue_books_details('Librarian')
        
        # Get recent transactions
        recent_transactions = DashboardModel.get_recent_transactions('Librarian')
        
        if stats is None:
            flash('Unable to load dashboard statistics', 'error')
            stats = {}
        
        return render_template(
            'dashboard_librarian.html',
            user=session,
            stats=stats,
            notifications=notifications,
            overdue_books=overdue_books,
            recent_transactions=recent_transactions
        )
        
    except Exception as e:
        logging.error(f"Librarian dashboard error: {e}")
        flash('Dashboard loading failed', 'error')
        return render_template('dashboard_librarian.html', user=session, stats={})


@dashboard_bp.route('/student')
@login_required
def student_dashboard():
    """
    Student dashboard with personal library information
    """
    try:
        # Get student-specific statistics
        stats = DashboardModel.get_student_statistics(session['user_id'])
        
        # Get recent notifications
        notifications = DashboardModel.get_recent_notifications(
            session['user_id'], 
            'Student'
        )
        
        # Get overdue books details for this student
        overdue_books = DashboardModel.get_overdue_books_details(
            'Student', 
            session['user_id']
        )
        
        # Get recent transactions for this student
        recent_transactions = DashboardModel.get_recent_transactions(
            'Student', 
            session['user_id']
        )
        
        if stats is None:
            flash('Unable to load dashboard statistics', 'error')
            stats = {}
        
        return render_template(
            'dashboard_student.html',
            user=session,
            stats=stats,
            notifications=notifications,
            overdue_books=overdue_books,
            recent_transactions=recent_transactions
        )
        
    except Exception as e:
        logging.error(f"Student dashboard error: {e}")
        flash('Dashboard loading failed', 'error')
        return render_template('dashboard_student.html', user=session, stats={})


@dashboard_bp.route('/api/stats')
@login_required
def api_stats():
    """
    API endpoint to get dashboard statistics in JSON format
    """
    try:
        user_role = session.get('user_role')
        user_id = session.get('user_id')
        
        if user_role == 'Admin':
            stats = DashboardModel.get_system_statistics()
        elif user_role == 'Librarian':
            stats = DashboardModel.get_librarian_statistics()
        else:  # Student
            stats = DashboardModel.get_student_statistics(user_id)
        
        if stats is None:
            return jsonify({'error': 'Unable to fetch statistics'}), 500
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logging.error(f"API stats error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@dashboard_bp.route('/api/notifications')
@login_required
def api_notifications():
    """
    API endpoint to get notifications in JSON format
    """
    try:
        user_role = session.get('user_role')
        user_id = session.get('user_id')
        
        notifications = DashboardModel.get_recent_notifications(user_id, user_role)
        
        return jsonify({
            'success': True,
            'notifications': notifications
        })
        
    except Exception as e:
        logging.error(f"API notifications error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@dashboard_bp.route('/api/overdue-books')
@login_required
def api_overdue_books():
    """
    API endpoint to get overdue books in JSON format
    """
    try:
        user_role = session.get('user_role')
        user_id = session.get('user_id')
        
        if user_role == 'Student':
            overdue_books = DashboardModel.get_overdue_books_details('Student', user_id)
        else:
            overdue_books = DashboardModel.get_overdue_books_details(user_role)
        
        return jsonify({
            'success': True,
            'overdue_books': overdue_books
        })
        
    except Exception as e:
        logging.error(f"API overdue books error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@dashboard_bp.route('/notifications/mark-read/<int:notification_id>')
@login_required
def mark_notification_read(notification_id):
    """
    Mark a notification as read
    
    Args:
        notification_id (int): ID of notification to mark as read
    """
    try:
        success = DashboardModel.mark_notification_read(notification_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Notification marked as read'})
        else:
            return jsonify({'success': False, 'message': 'Failed to mark notification as read'}), 400
        
    except Exception as e:
        logging.error(f"Mark notification read error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@dashboard_bp.route('/quick-access')
@login_required
def quick_access():
    """
    Display quick access menu for different modules
    """
    user_role = session.get('user_role')
    
    # Define module access based on role
    modules = {
        'Admin': [
            {'name': 'User Management', 'url': '#', 'icon': 'users'},
            {'name': 'Book Management', 'url': '#', 'icon': 'book'},
            {'name': 'Member Management', 'url': '#', 'icon': 'user-friends'},
            {'name': 'Transaction Reports', 'url': '#', 'icon': 'chart-bar'},
            {'name': 'System Settings', 'url': '#', 'icon': 'cog'},
            {'name': 'Reservations', 'url': '#', 'icon': 'bookmark'},
        ],
        'Librarian': [
            {'name': 'Book Management', 'url': '#', 'icon': 'book'},
            {'name': 'Issue/Return Books', 'url': '#', 'icon': 'exchange-alt'},
            {'name': 'Member Management', 'url': '#', 'icon': 'user-friends'},
            {'name': 'Reservations', 'url': '#', 'icon': 'bookmark'},
            {'name': 'Reports', 'url': '#', 'icon': 'chart-line'},
        ],
        'Student': [
            {'name': 'Search Books', 'url': '#', 'icon': 'search'},
            {'name': 'My Books', 'url': '#', 'icon': 'book-reader'},
            {'name': 'Reservations', 'url': '#', 'icon': 'bookmark'},
            {'name': 'My Profile', 'url': url_for('user.profile'), 'icon': 'user'},
        ]
    }
    
    user_modules = modules.get(user_role, modules['Student'])
    
    return render_template(
        'quick_access.html',
        user=session,
        modules=user_modules
    )


@dashboard_bp.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors"""
    flash('You do not have permission to access this page', 'error')
    return redirect(url_for('dashboard.student_dashboard'))


@dashboard_bp.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    flash('Page not found', 'error')
    return redirect(url_for('dashboard.dashboard'))
