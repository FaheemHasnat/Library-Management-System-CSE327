from flask import render_template, request, redirect, url_for, session, flash
from app.models.book import Book
from app.models.issued_book import IssuedBook
from app.utils.database import Database
from datetime import datetime


class LibrarianController:
    @staticmethod
    def librarian_dashboard():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        return render_template('dashboard/librarian_dashboard.html', 
                             user_name=session.get('user_name'))
    
    @staticmethod
    def book_management():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        subject_filter = request.args.get('subject', 'all')
        sort_by = request.args.get('sort', 'title')
        
        if request.method == 'POST':
            action = request.form.get('action')
            
            if action == 'add':
                title = request.form.get('title')
                author = request.form.get('author')
                subject = request.form.get('subject')
                isbn = request.form.get('isbn')
                
                if all([title, author, subject, isbn]):
                    if Book.add_book(title, author, subject, isbn):
                        flash('Book added successfully!', 'success')
                    else:
                        flash('Error adding book. Please try again.', 'error')
                else:
                    flash('Please fill in all fields', 'error')
                
                return redirect(url_for('librarian_book_management'))
            
            elif action == 'delete':
                book_id = request.form.get('book_id')
                result = Book.delete_book(book_id)
                
                if result == True:
                    flash('Book deleted successfully!', 'success')
                elif result == "borrowed":
                    flash('Cannot delete book - it is currently borrowed', 'error')
                else:
                    flash('Error deleting book. Please try again.', 'error')
                
                return redirect(url_for('librarian_book_management'))
            
            elif action == 'edit':
                book_id = request.form.get('book_id')
                title = request.form.get('title')
                author = request.form.get('author')
                subject = request.form.get('subject')
                isbn = request.form.get('isbn')
                
                if all([book_id, title, author, subject, isbn]):
                    if Book.update_book(book_id, title, author, subject, isbn):
                        flash('Book updated successfully!', 'success')
                    else:
                        flash('Error updating book. Please try again.', 'error')
                else:
                    flash('Please fill in all fields', 'error')
                
                return redirect(url_for('librarian_book_management'))
        
        books = Book.get_all_books_with_filter(subject_filter, sort_by)
        subjects = Book.get_all_subjects()
        
        return render_template('librarian/book_management.html', 
                             user_name=session.get('user_name'),
                             books=books,
                             subjects=subjects,
                             current_subject=subject_filter,
                             current_sort=sort_by)
    
    @staticmethod
    def book_issue():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            book_id = request.form.get('book_id')
            user_id = request.form.get('user_id')
            
            if not book_id or not user_id:
                flash('Please select both book and student', 'error')
            else:
                result = IssuedBook.issue_book(user_id, book_id)
                if result == True:
                    flash('Book issued successfully', 'success')
                elif result == "limit_exceeded":
                    flash('This student has already borrowed 3 books and cannot take another one', 'error')
                else:
                    flash('Failed to issue book', 'error')
            
            return redirect(url_for('librarian_book_issue'))
        
        books = IssuedBook.get_available_books()
        students = IssuedBook.get_students()
        
        for student in students:
            student['borrowed_count'] = IssuedBook.get_student_borrowed_count(student['UserID'])
        
        issued_books = IssuedBook.get_all_issued_books()
        
        return render_template('librarian/book_issue.html', 
                             user_name=session.get('user_name'),
                             books=books,
                             students=students,
                             issued_books=issued_books)
    
    @staticmethod
    def book_return():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            book_id = request.form.get('book_id')
            return_date = request.form.get('return_date')
            
            if not user_id or not book_id or not return_date:
                flash('Please provide user ID, book ID and return date', 'error')
            else:
                result = IssuedBook.return_book(user_id, book_id, return_date)
                if result and isinstance(result, dict) and result.get('success'):
                    fine_amount = result.get('fine', 0)
                    if fine_amount > 0:
                        flash(f'Book returned successfully. Fine: {fine_amount} Taka for late return', 'warning')
                    else:
                        flash('Book returned successfully', 'success')
                else:
                    flash('Failed to return book. Please check if the book was issued to this student', 'error')
            
            return redirect(url_for('librarian_book_return'))
        
        issued_books = IssuedBook.get_all_issued_books()
        today = datetime.now().date()
        
        return render_template('librarian/book_return.html', 
                             user_name=session.get('user_name'),
                             issued_books=issued_books,
                             today=today)
    
    @staticmethod
    def transaction_history():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        transactions = IssuedBook.get_transaction_history()
        
        return render_template('librarian/transaction_history.html',
                             user_name=session.get('user_name'),
                             transactions=transactions)
    
    @staticmethod
    def book_issue_return():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        return render_template('librarian/book_issue_return.html', user_name=session.get('user_name'))
    
    @staticmethod
    def notification_system():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        return render_template('librarian/notification_system.html', user_name=session.get('user_name'))
    
    @staticmethod
    def book_status():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        books = Book.get_all_books()
        
        return render_template('librarian/book_status.html', 
                             user_name=session.get('user_name'),
                             books=books)
    
    @staticmethod
    def fines_management():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        users_with_fines = IssuedBook.get_users_with_fines()
        fines_summary = IssuedBook.get_fines_summary()
        
        return render_template('librarian/fines_management.html', 
                             user_name=session.get('user_name'),
                             users_with_fines=users_with_fines,
                             fines_summary=fines_summary)
    
    @staticmethod
    def book_reservation():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            selected_books = request.form.getlist('selected_books')
            student_id = request.form.get('student_id')
            
            if not selected_books:
                flash('Please select at least one book', 'error')
            elif not student_id:
                flash('Please select a student', 'error')
            elif len(selected_books) > 3:
                flash('You can select maximum 3 books at a time', 'error')
            else:
                current_reservations = Book.get_student_reservation_count(student_id)
                total_after_reservation = current_reservations + len(selected_books)
                
                if total_after_reservation > 3:
                    flash(f'Student already has {current_reservations} reservations. Cannot reserve {len(selected_books)} more books (limit: 3)', 'error')
                else:
                    success_count = 0
                    failed_books = []
                    
                    for book_id in selected_books:
                        result = Book.create_reservation(book_id, student_id)
                        if result == True:
                            success_count += 1
                        elif result == "limit_exceeded":
                            flash('Student has reached the reservation limit of 3 books', 'error')
                            break
                        else:
                            book = Book.get_book_by_id(book_id)
                            if book:
                                failed_books.append(book['title'])
                    
                    if success_count > 0:
                        if success_count == len(selected_books):
                            flash(f'All {success_count} book reservations created successfully', 'success')
                        else:
                            flash(f'{success_count} out of {len(selected_books)} reservations created successfully', 'warning')
                            if failed_books:
                                flash(f'Failed to reserve: {", ".join(failed_books)}', 'error')
                    else:
                        flash('Failed to create reservations. Books may already be reserved or unavailable', 'error')
        
        books = Book.get_all_books_with_filter('all', 'title')
        available_books = [book for book in books if book['status'] == 'Available']
        
        try:
            students_query = "SELECT UserID as user_id, Name as full_name, Email as email FROM users WHERE Role = 'Student'"
            students = Database.execute_query(students_query) or []
        except:
            students = []
        
        try:
            reservations_query = """
            SELECT br.reservation_id, b.title, u.Name as full_name, br.reservation_date 
            FROM book_reservations br 
            JOIN books b ON br.book_id = b.book_id 
            JOIN users u ON br.user_id = u.UserID 
            WHERE br.status = 'Active' 
            ORDER BY br.reservation_date DESC LIMIT 10
            """
            reservations = Database.execute_query(reservations_query) or []
        except:
            reservations = []
        
        return render_template('librarian/book_reservation.html', 
                             user_name=session.get('user_name'),
                             books=available_books,
                             students=students,
                             reservations=reservations)
