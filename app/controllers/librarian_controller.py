from flask import render_template, request, redirect, url_for, session, flash
from app.models.book import Book
from app.models.issued_book import IssuedBook


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
        
        return render_template('librarian/book_management.html', user_name=session.get('user_name'))
    
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
            student_email = request.form.get('student_email')
            book_id = request.form.get('book_id')
            
            if not student_email or not book_id:
                flash('Please provide both student email and book ID', 'error')
            else:
                user = Book.get_user_by_email(student_email)
                if not user:
                    flash('Student not found', 'error')
                else:
                    if IssuedBook.return_book(user['user_id'], book_id):
                        flash('Book returned successfully', 'success')
                    else:
                        flash('Failed to return book. Please check if the book was issued to this student', 'error')
            
            return redirect(url_for('librarian_book_return'))
        
        issued_books = IssuedBook.get_all_issued_books()
        
        return render_template('librarian/book_return.html', 
                             user_name=session.get('user_name'),
                             issued_books=issued_books)
    
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
        
        return render_template('librarian/fines_management.html', user_name=session.get('user_name'))
    
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
            elif not Book.validate_student_id(student_id):
                flash('Invalid student selected', 'error')
            else:
                success_count = Book.create_multiple_reservations(selected_books, student_id)
                if success_count > 0:
                    if success_count == len(selected_books):
                        flash(f'All {success_count} book reservations created successfully', 'success')
                    else:
                        flash(f'{success_count} out of {len(selected_books)} reservations created successfully', 'warning')
                else:
                    flash('Failed to create reservations. Books may already be reserved by this student', 'error')
        
        books = Book.get_all_available_books()
        students = Book.get_all_students()
        reservations = Book.get_recent_reservations()
        
        return render_template('librarian/book_reservation.html', 
                             user_name=session.get('user_name'),
                             books=books,
                             students=students,
                             reservations=reservations)
