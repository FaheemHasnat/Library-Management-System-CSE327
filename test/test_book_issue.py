import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.controllers.librarian_controller import LibrarianController
from app.models.issued_book import IssuedBook


class TestBookIssue:
    
    @pytest.fixture
    def mock_session(self):
        with patch('app.controllers.librarian_controller.session') as mock:
            mock.get.side_effect = lambda key, default=None: {
                'user_id': 'lib-001',
                'user_role': 'Librarian',
                'user_name': 'Test Librarian'
            }.get(key, default)
            yield mock
    
    @pytest.fixture
    def mock_issued_book(self):
        with patch('app.controllers.librarian_controller.IssuedBook') as mock:
            yield mock
    
    @pytest.fixture
    def mock_flash(self):
        with patch('app.controllers.librarian_controller.flash') as mock:
            yield mock
    
    @pytest.fixture
    def mock_redirect(self):
        with patch('app.controllers.librarian_controller.redirect') as mock:
            yield mock
    
    @pytest.fixture
    def mock_render_template(self):
        with patch('app.controllers.librarian_controller.render_template') as mock:
            yield mock

    @pytest.fixture
    def mock_url_for(self):
        with patch('app.controllers.librarian_controller.url_for') as mock:
            yield mock

    def test_librarian_dashboard_access_granted(self, mock_session, mock_render_template):
        result = LibrarianController.librarian_dashboard()
        
        mock_render_template.assert_called_once_with(
            'dashboard/librarian_dashboard.html',
            user_name='Test Librarian'
        )

    def test_librarian_dashboard_access_denied_no_session(self, mock_flash, mock_redirect):
        with patch('app.controllers.librarian_controller.session') as mock_session:
            mock_session.get.side_effect = lambda key, default=None: {}.get(key, default)
            
            result = LibrarianController.librarian_dashboard()
        
        mock_flash.assert_called_once_with('Access denied', 'error')

    def test_librarian_dashboard_access_denied_wrong_role(self, mock_flash, mock_redirect):
        with patch('app.controllers.librarian_controller.session') as mock_session:
            mock_session.get.side_effect = lambda key, default=None: {
                'user_id': 'user-001',
                'user_role': 'Student'
            }.get(key, default)
            
            result = LibrarianController.librarian_dashboard()
        
        mock_flash.assert_called_once_with('Access denied', 'error')

    @patch('app.controllers.librarian_controller.request')
    def test_book_issue_get_request(self, mock_request, mock_session, mock_issued_book, mock_render_template):
        mock_request.method = 'GET'
        
        mock_books = [
            {'book_id': '1', 'title': 'Python Programming', 'author': 'John Smith', 'isbn': '123456789'},
            {'book_id': '2', 'title': 'Web Development', 'author': 'Jane Doe', 'isbn': '987654321'}
        ]
        mock_students = [
            {'UserID': 'student-1', 'student_name': 'Alice Johnson'},
            {'UserID': 'student-2', 'student_name': 'Bob Wilson'}
        ]
        mock_issued_books = [
            {'book_id': '3', 'UserID': 'student-1', 'title': 'Database Design', 'student_name': 'Alice Johnson'}
        ]
        
        mock_issued_book.get_available_books.return_value = mock_books
        mock_issued_book.get_students.return_value = mock_students
        mock_issued_book.get_all_issued_books.return_value = mock_issued_books
        mock_issued_book.get_student_borrowed_count.return_value = 1
        
        result = LibrarianController.book_issue()
        
        mock_render_template.assert_called_once()
        args, kwargs = mock_render_template.call_args
        assert args[0] == 'librarian/book_issue.html'
        assert kwargs['user_name'] == 'Test Librarian'
        assert kwargs['books'] == mock_books
        assert kwargs['issued_books'] == mock_issued_books

    @patch('app.controllers.librarian_controller.request')
    def test_book_issue_post_success(self, mock_request, mock_session, mock_issued_book, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'book_id': 'book-123',
            'user_id': 'student-456'
        }.get(key)
        
        mock_issued_book.issue_book.return_value = True
        mock_url_for.return_value = '/librarian/book-issue'
        
        result = LibrarianController.book_issue()
        
        mock_issued_book.issue_book.assert_called_once_with('student-456', 'book-123')
        mock_flash.assert_called_once_with('Book issued successfully', 'success')
        mock_redirect.assert_called_once()

    @patch('app.controllers.librarian_controller.request')
    def test_book_issue_post_limit_exceeded(self, mock_request, mock_session, mock_issued_book, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'book_id': 'book-123',
            'user_id': 'student-456'
        }.get(key)
        
        mock_issued_book.issue_book.return_value = "limit_exceeded"
        mock_url_for.return_value = '/librarian/book-issue'
        
        result = LibrarianController.book_issue()
        
        mock_flash.assert_called_once_with('This student has already borrowed 3 books and cannot take another one', 'error')

    @patch('app.controllers.librarian_controller.request')
    def test_book_issue_post_failure(self, mock_request, mock_session, mock_issued_book, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'book_id': 'book-123',
            'user_id': 'student-456'
        }.get(key)
        
        mock_issued_book.issue_book.return_value = False
        mock_url_for.return_value = '/librarian/book-issue'
        
        result = LibrarianController.book_issue()
        
        mock_flash.assert_called_once_with('Failed to issue book', 'error')

    @patch('app.controllers.librarian_controller.request')
    def test_book_issue_post_missing_book_id(self, mock_request, mock_session, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'book_id': None,
            'user_id': 'student-456'
        }.get(key)
        
        mock_url_for.return_value = '/librarian/book-issue'
        
        result = LibrarianController.book_issue()
        
        mock_flash.assert_called_once_with('Please select both book and student', 'error')

    @patch('app.controllers.librarian_controller.request')
    def test_book_issue_post_missing_user_id(self, mock_request, mock_session, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'book_id': 'book-123',
            'user_id': None
        }.get(key)
        
        mock_url_for.return_value = '/librarian/book-issue'
        
        result = LibrarianController.book_issue()
        
        mock_flash.assert_called_once_with('Please select both book and student', 'error')

    def test_issue_book_model_success(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        mock_cursor.fetchone.side_effect = [
            (2,),
            ('Available',)
        ]
        
        with patch('app.models.issued_book.Database.get_connection', return_value=mock_connection):
            with patch('app.models.issued_book.datetime') as mock_datetime:
                mock_datetime.now.return_value.date.return_value = 'mock_date'
                mock_datetime.timedelta.return_value = 'mock_due_date'
                
                result = IssuedBook.issue_book('student-123', 'book-456')
        
        assert result is True
        assert mock_cursor.execute.call_count == 4

    def test_issue_book_model_limit_exceeded(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        mock_cursor.fetchone.return_value = (3,)
        
        with patch('app.models.issued_book.Database.get_connection', return_value=mock_connection):
            result = IssuedBook.issue_book('student-123', 'book-456')
        
        assert result == "limit_exceeded"

    def test_issue_book_model_book_not_available(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        mock_cursor.fetchone.side_effect = [
            (1,),
            ('Borrowed',)
        ]
        
        with patch('app.models.issued_book.Database.get_connection', return_value=mock_connection):
            result = IssuedBook.issue_book('student-123', 'book-456')
        
        assert result is False

    def test_issue_book_model_no_connection(self):
        with patch('app.models.issued_book.Database.get_connection', return_value=None):
            result = IssuedBook.issue_book('student-123', 'book-456')
        
        assert result is False

    def test_get_available_books(self):
        mock_books = [
            {'book_id': '1', 'title': 'Python Programming', 'author': 'John Smith', 'isbn': '123456789'},
            {'book_id': '2', 'title': 'Web Development', 'author': 'Jane Doe', 'isbn': '987654321'}
        ]
        
        with patch('app.models.issued_book.Database.execute_query', return_value=mock_books):
            result = IssuedBook.get_available_books()
        
        assert result == mock_books

    def test_get_available_books_no_books(self):
        with patch('app.models.issued_book.Database.execute_query', return_value=None):
            result = IssuedBook.get_available_books()
        
        assert result == []

    def test_get_students(self):
        mock_students = [
            {'UserID': 'student-1', 'student_name': 'Alice Johnson'},
            {'UserID': 'student-2', 'student_name': 'Bob Wilson'}
        ]
        
        with patch('app.models.issued_book.Database.execute_query', return_value=mock_students):
            result = IssuedBook.get_students()
        
        assert result == mock_students

    def test_get_students_no_students(self):
        with patch('app.models.issued_book.Database.execute_query', return_value=None):
            result = IssuedBook.get_students()
        
        assert result == []

    def test_get_student_borrowed_count(self):
        mock_result = {'count': 2}
        
        with patch('app.models.issued_book.Database.execute_single_query', return_value=mock_result):
            result = IssuedBook.get_student_borrowed_count('student-123')
        
        assert result == 2

    def test_get_student_borrowed_count_no_result(self):
        with patch('app.models.issued_book.Database.execute_single_query', return_value=None):
            result = IssuedBook.get_student_borrowed_count('student-123')
        
        assert result == 0

    def test_get_all_issued_books(self):
        mock_issued_books = [
            {
                'book_id': '1',
                'UserID': 'student-1',
                'title': 'Python Programming',
                'student_name': 'Alice Johnson',
                'issue_date': '2025-08-10',
                'due_date': '2025-08-17'
            }
        ]
        
        with patch('app.models.issued_book.Database.execute_query', return_value=mock_issued_books):
            result = IssuedBook.get_all_issued_books()
        
        assert result == mock_issued_books

    def test_get_all_issued_books_no_books(self):
        with patch('app.models.issued_book.Database.execute_query', return_value=None):
            result = IssuedBook.get_all_issued_books()
        
        assert result == []
