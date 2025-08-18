from flask import render_template, request, redirect, url_for, session, flash
from app.models.book import Book
from app.utils.database import Database


class LibrarianController:
    @staticmethod
    def librarian_dashboard():
        if 'user_id' not in session or session.get('user_role') != 'Librarian':
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        
        return render_template('dashboard/librarian_dashboard.html', 
                             user_name=session.get('user_name'))
    
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
