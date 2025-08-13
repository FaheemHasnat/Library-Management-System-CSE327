
from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from functools import wraps
from app.models.reservation_model import ReservationModel
from app.models.user_model import UserModel
import logging

reservation_bp = Blueprint('reservation', __name__, url_prefix='/reservation')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session:
                flash('Access denied.', 'error')
                return redirect(url_for('user.login'))
            
            if session['user_role'] not in allowed_roles:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('dashboard.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@reservation_bp.route('/')
@login_required
def index():
    try:
        user_id = session.get('user_id')
        user_role = session.get('user_role')
        
        if user_role in ['Admin', 'Librarian']:
            reservations = ReservationModel.get_all_reservations()
            template = 'reservation/manage_reservations.html'
        else:
            reservations = ReservationModel.get_user_reservations(user_id)
            template = 'reservation/my_reservations.html'
        
        return render_template(template, reservations=reservations)
        
    except Exception as e:
        logging.error(f"Reservation index error: {e}")
        flash('An error occurred while loading reservations.', 'error')
        return redirect(url_for('dashboard.dashboard'))


@reservation_bp.route('/reserve', methods=['POST'])
@login_required
def reserve_book():
    try:
        user_id = session.get('user_id')
        book_id = request.form.get('book_id')
        
        if not book_id:
            flash('Book ID is required.', 'error')
            return redirect(request.referrer or url_for('dashboard.dashboard'))
        
        result = ReservationModel.reserve_book(user_id, book_id)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
        
        return redirect(request.referrer or url_for('dashboard.dashboard'))
        
    except Exception as e:
        logging.error(f"Reserve book error: {e}")
        flash('An error occurred while processing your reservation.', 'error')
        return redirect(request.referrer or url_for('dashboard.dashboard'))


@reservation_bp.route('/reserve-multiple', methods=['POST'])
@login_required
def reserve_multiple_books():
    try:
        user_id = session.get('user_id')
        book_ids = request.form.getlist('book_ids')
        
        if not book_ids:
            flash('Please select at least one book to reserve.', 'error')
            return redirect(request.referrer or url_for('search.books'))
        
        success_count = 0
        error_messages = []
        
        for book_id in book_ids:
            result = ReservationModel.reserve_book(user_id, book_id)
            if result['success']:
                success_count += 1
            else:
                error_messages.append(f"Book ID {book_id}: {result['message']}")
        
        if success_count > 0:
            flash(f'Successfully reserved {success_count} book(s).', 'success')
        
        if error_messages:
            for error in error_messages[:3]:
                flash(error, 'error')
            if len(error_messages) > 3:
                flash(f'...and {len(error_messages) - 3} more errors.', 'error')
        
        return redirect(url_for('reservation.my_reservations'))
        
    except Exception as e:
        logging.error(f"Reserve multiple books error: {e}")
        flash('An error occurred while processing your reservations.', 'error')
        return redirect(request.referrer or url_for('search.books'))


@reservation_bp.route('/cancel', methods=['POST'])
@login_required
def cancel_reservation():
    try:
        user_id = session.get('user_id')
        reservation_id = request.form.get('reservation_id')
        
        if not reservation_id:
            flash('Reservation ID is required.', 'error')
            return redirect(request.referrer or url_for('reservation.index'))
        
        result = ReservationModel.cancel_reservation(reservation_id, user_id)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
        
        return redirect(url_for('reservation.index'))
        
    except Exception as e:
        logging.error(f"Cancel reservation error: {e}")
        flash('An error occurred while cancelling your reservation.', 'error')
        return redirect(url_for('reservation.index'))


@reservation_bp.route('/queue/<book_id>')
@login_required
@role_required(['Admin', 'Librarian'])
def view_queue(book_id):
    try:
        queue = ReservationModel.check_reservation_queue(book_id)
        book_info = ReservationModel._get_book_info(book_id)
        
        return render_template(
            'reservation/queue.html',
            queue=queue,
            book_info=book_info
        )
        
    except Exception as e:
        logging.error(f"View queue error: {e}")
        flash('An error occurred while loading the reservation queue.', 'error')
        return redirect(url_for('reservation.index'))


@reservation_bp.route('/api/reserve', methods=['POST'])
@login_required
def api_reserve_book():
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        book_id = data.get('book_id') if data else None
        
        if not book_id:
            return jsonify({
                'success': False,
                'message': 'Book ID is required'
            }), 400
        
        result = ReservationModel.reserve_book(user_id, book_id)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logging.error(f"API reserve book error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your reservation'
        }), 500


@reservation_bp.route('/api/cancel', methods=['POST'])
@login_required
def api_cancel_reservation():
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        reservation_id = data.get('reservation_id') if data else None
        
        if not reservation_id:
            return jsonify({
                'success': False,
                'message': 'Reservation ID is required'
            }), 400
        
        result = ReservationModel.cancel_reservation(reservation_id, user_id)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logging.error(f"API cancel reservation error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while cancelling your reservation'
        }), 500


@reservation_bp.route('/api/queue/<book_id>')
@login_required
@role_required(['Admin', 'Librarian'])
def api_get_queue(book_id):
    try:
        queue = ReservationModel.check_reservation_queue(book_id)
        
        return jsonify({
            'success': True,
            'queue': queue
        })
        
    except Exception as e:
        logging.error(f"API get queue error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while loading the queue'
        }), 500


@reservation_bp.route('/api/statistics')
@login_required
@role_required(['Admin', 'Librarian'])
def api_get_statistics():
    try:
        stats = ReservationModel.get_reservation_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        logging.error(f"API get statistics error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while loading statistics'
        }), 500


@reservation_bp.route('/manage')
@login_required
@role_required(['Admin', 'Librarian'])
def manage_reservations():
    try:
        reservations = ReservationModel.get_all_reservations(limit=100)
        statistics = ReservationModel.get_reservation_statistics()
        
        return render_template(
            'reservation/manage_reservations.html',
            reservations=reservations,
            statistics=statistics
        )
        
    except Exception as e:
        logging.error(f"Manage reservations error: {e}")
        flash('An error occurred while loading reservations management.', 'error')
        return redirect(url_for('dashboard.dashboard'))


@reservation_bp.route('/my-reservations')
@login_required
def my_reservations():
    try:
        user_id = session.get('user_id')
        reservations = ReservationModel.get_user_reservations(user_id)
        
        return render_template(
            'reservation/my_reservations.html',
            reservations=reservations
        )
        
    except Exception as e:
        logging.error(f"My reservations error: {e}")
        flash('An error occurred while loading your reservations.', 'error')
        return redirect(url_for('dashboard.dashboard'))


@reservation_bp.route('/process-return', methods=['POST'])
@login_required
@role_required(['Admin', 'Librarian'])
def process_book_return():
    try:
        book_id = request.form.get('book_id')
        
        if not book_id:
            flash('Book ID is required.', 'error')
            return redirect(request.referrer or url_for('dashboard.dashboard'))
        
        result = ReservationModel.process_book_return(book_id)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
        
        return redirect(request.referrer or url_for('dashboard.dashboard'))
        
    except Exception as e:
        logging.error(f"Process book return error: {e}")
        flash('An error occurred while processing the book return.', 'error')
        return redirect(request.referrer or url_for('dashboard.dashboard'))


@reservation_bp.errorhandler(404)
def not_found(error):
    flash('The requested reservation page was not found.', 'error')
    return redirect(url_for('reservation.index'))


@reservation_bp.errorhandler(500)
def internal_error(error):
    logging.error(f"Reservation internal error: {error}")
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('reservation.index'))
