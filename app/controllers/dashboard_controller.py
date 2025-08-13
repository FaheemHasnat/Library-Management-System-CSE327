from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from app.models.dashboard_model import DashboardModel
from app.controllers.user_controller import login_required, role_required
import logging

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_role = session.get('user_role')
    
    if user_role == 'Admin':
        return redirect(url_for('dashboard.admin_dashboard'))
    elif user_role == 'Librarian':
        return redirect(url_for('dashboard.librarian_dashboard'))
    else:
        return redirect(url_for('dashboard.student_dashboard'))


@dashboard_bp.route('/admin')
@login_required
@role_required(['Admin'])
def admin_dashboard():
    try:
        stats = DashboardModel.get_system_statistics()
        
        notifications = DashboardModel.get_recent_notifications(
            session['user_id'], 
            'Admin'
        )
        
        overdue_books = DashboardModel.get_overdue_books_details('Admin')
        
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
    try:
        stats = DashboardModel.get_librarian_statistics()
        
        notifications = DashboardModel.get_recent_notifications(
            session['user_id'], 
            'Librarian'
        )
        
        overdue_books = DashboardModel.get_overdue_books_details('Librarian')
        
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
    try:
        stats = DashboardModel.get_student_statistics(session['user_id'])
        
        notifications = DashboardModel.get_recent_notifications(
            session['user_id'], 
            'Student'
        )
        
        overdue_books = DashboardModel.get_overdue_books_details(
            'Student', 
            session['user_id']
        )
        
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
    try:
        user_role = session.get('user_role')
        user_id = session.get('user_id')
        
        if user_role == 'Admin':
            stats = DashboardModel.get_system_statistics()
        elif user_role == 'Librarian':
            stats = DashboardModel.get_librarian_statistics()
        else:
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
    user_role = session.get('user_role')
    
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
    flash('You do not have permission to access this page', 'error')
    return redirect(url_for('dashboard.student_dashboard'))


@dashboard_bp.errorhandler(404)
def not_found(error):
    flash('Page not found', 'error')
    return redirect(url_for('dashboard.dashboard'))
