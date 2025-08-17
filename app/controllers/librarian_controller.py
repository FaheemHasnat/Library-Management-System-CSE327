from flask import render_template, request, redirect, url_for, session, flash
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
