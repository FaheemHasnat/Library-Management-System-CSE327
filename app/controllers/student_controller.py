from flask import render_template, request, redirect, url_for, session, flash
from app.models.book import Book
from app.models.issued_book import IssuedBook


class StudentController:
    @staticmethod
    def student_dashboard():
        if 'user_id' not in session or session.get('user_role') != 'Student':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        user_reservation_count = Book.get_user_reservation_count(user_id)
        student_fines = IssuedBook.get_student_fines(user_id)
        
        dummy_stats = {
            'issued_books': 3,
            'available_books': 1247,
            'pending_fines': student_fines,
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
    
    @staticmethod
    def book_status():
        if 'user_id' not in session or session.get('user_role') != 'Student':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        books = Book.get_all_books()
        
        return render_template('student/book_status.html', 
                             user_name=session.get('user_name'),
                             books=books)
    
    @staticmethod
    def book_reservation():
        if 'user_id' not in session or session.get('user_role') != 'Student':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        current_reservation_count = Book.get_user_reservation_count(user_id)
        
        if request.method == 'POST':
            selected_books = request.form.getlist('selected_books')
            
            if not selected_books:
                flash('Please select at least one book', 'error')
            elif current_reservation_count >= 3:
                flash('You already have 3 book reservations. Cannot reserve more books.', 'error')
            elif current_reservation_count + len(selected_books) > 3:
                remaining_slots = 3 - current_reservation_count
                flash(f'You can only reserve {remaining_slots} more book(s). You selected {len(selected_books)} books.', 'error')
            else:
                success_count = Book.create_multiple_reservations(selected_books, user_id)
                if success_count > 0:
                    if success_count == len(selected_books):
                        flash(f'All {success_count} book reservations created successfully', 'success')
                    else:
                        flash(f'{success_count} out of {len(selected_books)} reservations created successfully', 'warning')
                    current_reservation_count = Book.get_user_reservation_count(user_id)
                else:
                    flash('Failed to create reservations. Books may already be reserved by you or not available', 'error')
        
        books = Book.get_all_available_books()
        user_reservations = Book.get_user_reservations(user_id)
        remaining_slots = 3 - current_reservation_count
        
        return render_template('student/book_reservation.html', 
                             user_name=session.get('user_name'),
                             books=books,
                             user_reservations=user_reservations,
                             remaining_slots=remaining_slots)
    
    @staticmethod
    def account_status():
        if 'user_id' not in session or session.get('user_role') != 'Student':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        user_id = session.get('user_id')
        total_fines = IssuedBook.get_student_fines(user_id)
        fine_history = IssuedBook.get_student_fine_history(user_id)
        
        formatted_fine_history = []
        for record in fine_history:
            formatted_fine_history.append({
                'description': f'Late return - {record["book_title"]}',
                'amount': record['Fine'],
                'date': record['ReturnDate'].strftime('%Y-%m-%d') if record['ReturnDate'] else 'N/A',
                'status': 'Pending'
            })
        
        dummy_account = {
            'total_fines': total_fines,
            'paid_fines': 0.00,
            'pending_fines': total_fines,
            'account_status': 'Active'
        }
        
        return render_template('student/account_status.html', 
                             user_name=session.get('user_name'),
                             account=dummy_account,
                             fine_history=formatted_fine_history)
    
    @staticmethod
    def your_books():
        if 'user_id' not in session or session.get('user_role') != 'Student':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        dummy_borrowed_books = [
            {'id': 1, 'title': 'Python Programming', 'author': 'John Doe', 'issue_date': '2025-08-01', 'due_date': '2025-08-20'},
            {'id': 2, 'title': 'Data Structures', 'author': 'Jane Smith', 'issue_date': '2025-08-05', 'due_date': '2025-08-25'},
            {'id': 3, 'title': 'Algorithm Design', 'author': 'Bob Wilson', 'issue_date': '2025-07-28', 'due_date': '2025-08-18'}
        ]
        
        return render_template('student/your_books.html', 
                             user_name=session.get('user_name'),
                             borrowed_books=dummy_borrowed_books)
