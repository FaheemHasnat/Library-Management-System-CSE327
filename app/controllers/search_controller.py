
from flask import Blueprint, request, render_template, session, redirect, url_for, flash, jsonify
from app.controllers.user_controller import login_required
from app.utils.lms_db import DatabaseConnection
import logging

search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('/books')
@login_required
def books():
    try:
        title = request.args.get('title', '').strip()
        author = request.args.get('author', '').strip()
        subject = request.args.get('subject', '').strip()
        status = request.args.get('status', '').strip()
        
        logging.info(f"Books page accessed by user: {session.get('user_id', 'Unknown')}")
        
        db = DatabaseConnection()
        
        base_query = """
            SELECT BookID, Title, Author, Subject, ISBN, Status
            FROM book
            WHERE 1=1
        """
        
        params = []
        query_conditions = []
        
        if title:
            query_conditions.append("Title LIKE %s")
            params.append(f"%{title}%")
        
        if author:
            query_conditions.append("Author LIKE %s")
            params.append(f"%{author}%")
        
        if subject:
            query_conditions.append("Subject LIKE %s")
            params.append(f"%{subject}%")
        
        if status:
            query_conditions.append("Status = %s")
            params.append(status)
        
        if query_conditions:
            base_query += " AND " + " AND ".join(query_conditions)
        
        base_query += " ORDER BY Title ASC LIMIT 50"
        
        books = db.execute_query(base_query, tuple(params)) or []
        
        search_params = {
            'title': title,
            'author': author,
            'subject': subject,
            'status': status
        }
        
        return render_template(
            'search/books.html',
            books=books,
            search_params=search_params,
            user=session
        )
        
    except Exception as e:
        logging.error(f"Book search error: {e}")
        flash('An error occurred while searching for books', 'error')
        return render_template('search/books.html', books=[], search_params={}, user=session)


@search_bp.route('/api/books')
@login_required
def api_books():
    try:
        title = request.args.get('title', '').strip()
        author = request.args.get('author', '').strip()
        subject = request.args.get('subject', '').strip()
        status = request.args.get('status', '').strip()
        
        db = DatabaseConnection()
        
        base_query = """
            SELECT BookID, Title, Author, Subject, ISBN, Status
            FROM book
            WHERE 1=1
        """
        
        params = []
        query_conditions = []
        
        if title:
            query_conditions.append("Title LIKE %s")
            params.append(f"%{title}%")
        
        if author:
            query_conditions.append("Author LIKE %s")
            params.append(f"%{author}%")
        
        if subject:
            query_conditions.append("Subject LIKE %s")
            params.append(f"%{subject}%")
        
        if status:
            query_conditions.append("Status = %s")
            params.append(status)
        
        if query_conditions:
            base_query += " AND " + " AND ".join(query_conditions)
        
        base_query += " ORDER BY Title ASC LIMIT 50"
        
        books = db.execute_query(base_query, tuple(params)) or []
        
        return jsonify({
            'success': True,
            'books': books,
            'count': len(books)
        })
        
    except Exception as e:
        logging.error(f"API book search error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while searching for books',
            'books': []
        }), 500


@search_bp.route('/suggestions')
@login_required
def suggestions():
    try:
        query_type = request.args.get('type', 'title')
        term = request.args.get('term', '').strip()
        
        if not term or len(term) < 2:
            return jsonify({'suggestions': []})
        
        db = DatabaseConnection()
        
        suggestions = []
        
        if query_type == 'title':
            query = """
                SELECT DISTINCT Title
                FROM book
                WHERE Title LIKE %s
                ORDER BY Title ASC
                LIMIT 10
            """
            results = db.execute_query(query, (f"%{term}%",)) or []
            suggestions = [row['Title'] for row in results]
        
        elif query_type == 'author':
            query = """
                SELECT DISTINCT Author
                FROM book
                WHERE Author LIKE %s
                ORDER BY Author ASC
                LIMIT 10
            """
            results = db.execute_query(query, (f"%{term}%",)) or []
            suggestions = [row['Author'] for row in results]
        
        elif query_type == 'subject':
            query = """
                SELECT DISTINCT Subject
                FROM book
                WHERE Subject LIKE %s
                ORDER BY Subject ASC
                LIMIT 10
            """
            results = db.execute_query(query, (f"%{term}%",)) or []
            suggestions = [row['Subject'] for row in results]
        
        return jsonify({'suggestions': suggestions})
        
    except Exception as e:
        logging.error(f"Suggestions error: {e}")
        return jsonify({'suggestions': []})


@search_bp.route('/advanced')
@login_required
def advanced_search():
    try:
        return render_template('search/advanced.html', user=session)
        
    except Exception as e:
        logging.error(f"Advanced search page error: {e}")
        flash('Unable to load advanced search page', 'error')
        return redirect(url_for('search.books'))


@search_bp.route('/book/<int:book_id>')
@login_required
def book_details(book_id):
    try:
        db = DatabaseConnection()
        
        query = """
            SELECT BookID, Title, Author, Subject, ISBN, Status, Publisher, PublicationYear, Description
            FROM book
            WHERE BookID = %s
        """
        
        book = db.execute_query(query, (book_id,))
        
        if not book:
            flash('Book not found', 'error')
            return redirect(url_for('search.books'))
        
        book = book[0]
        
        availability_query = """
            SELECT COUNT(*) as total_copies,
                   SUM(CASE WHEN Status = 'Available' THEN 1 ELSE 0 END) as available_copies
            FROM book
            WHERE Title = %s AND Author = %s
        """
        
        availability = db.execute_query(availability_query, (book['Title'], book['Author']))
        availability = availability[0] if availability else {'total_copies': 0, 'available_copies': 0}
        
        return render_template(
            'search/book_details.html',
            book=book,
            availability=availability,
            user=session
        )
        
    except Exception as e:
        logging.error(f"Book details error: {e}")
        flash('Unable to load book details', 'error')
        return redirect(url_for('search.books'))
