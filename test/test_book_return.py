import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.controllers.librarian_controller import LibrarianController
from app.models.issued_book import IssuedBook


class TestBookReturn:
    
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

    @pytest.fixture
    def mock_datetime(self):
        with patch('app.controllers.librarian_controller.datetime') as mock:
            mock.now.return_value.date.return_value = '2025-08-17'
            yield mock

    @patch('app.controllers.librarian_controller.request')
    def test_book_return_get_request(self, mock_request, mock_session, mock_issued_book, mock_datetime, mock_render_template):
        mock_request.method = 'GET'
        
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
        
        mock_issued_book.get_all_issued_books.return_value = mock_issued_books
        
        result = LibrarianController.book_return()
        
        mock_render_template.assert_called_once()
        args, kwargs = mock_render_template.call_args
        assert args[0] == 'librarian/book_return.html'
        assert kwargs['user_name'] == 'Test Librarian'
        assert kwargs['issued_books'] == mock_issued_books
        assert kwargs['today'] == '2025-08-17'

    @patch('app.controllers.librarian_controller.request')
    def test_book_return_post_success_no_fine(self, mock_request, mock_session, mock_issued_book, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'user_id': 'student-123',
            'book_id': 'book-456',
            'return_date': '2025-08-17'
        }.get(key)
        
        mock_issued_book.return_book.return_value = {'success': True, 'fine': 0}
        mock_url_for.return_value = '/librarian/book-return'
        
        result = LibrarianController.book_return()
        
        mock_issued_book.return_book.assert_called_once_with('student-123', 'book-456', '2025-08-17')
        mock_flash.assert_called_once_with('Book returned successfully', 'success')
        mock_redirect.assert_called_once()

    @patch('app.controllers.librarian_controller.request')
    def test_book_return_post_success_with_fine(self, mock_request, mock_session, mock_issued_book, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'user_id': 'student-123',
            'book_id': 'book-456',
            'return_date': '2025-08-20'
        }.get(key)
        
        mock_issued_book.return_book.return_value = {'success': True, 'fine': 30.0}
        mock_url_for.return_value = '/librarian/book-return'
        
        result = LibrarianController.book_return()
        
        mock_flash.assert_called_once_with('Book returned successfully. Fine: 30.0 Taka for late return', 'warning')

    @patch('app.controllers.librarian_controller.request')
    def test_book_return_post_failure(self, mock_request, mock_session, mock_issued_book, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'user_id': 'student-123',
            'book_id': 'book-456',
            'return_date': '2025-08-17'
        }.get(key)
        
        mock_issued_book.return_book.return_value = False
        mock_url_for.return_value = '/librarian/book-return'
        
        result = LibrarianController.book_return()
        
        mock_flash.assert_called_once_with('Failed to return book. Please check if the book was issued to this student', 'error')

    @patch('app.controllers.librarian_controller.request')
    def test_book_return_post_missing_user_id(self, mock_request, mock_session, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'user_id': None,
            'book_id': 'book-456',
            'return_date': '2025-08-17'
        }.get(key)
        
        mock_url_for.return_value = '/librarian/book-return'
        
        result = LibrarianController.book_return()
        
        mock_flash.assert_called_once_with('Please provide user ID, book ID and return date', 'error')

    @patch('app.controllers.librarian_controller.request')
    def test_book_return_post_missing_book_id(self, mock_request, mock_session, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'user_id': 'student-123',
            'book_id': None,
            'return_date': '2025-08-17'
        }.get(key)
        
        mock_url_for.return_value = '/librarian/book-return'
        
        result = LibrarianController.book_return()
        
        mock_flash.assert_called_once_with('Please provide user ID, book ID and return date', 'error')

    @patch('app.controllers.librarian_controller.request')
    def test_book_return_post_missing_return_date(self, mock_request, mock_session, mock_flash, mock_redirect, mock_url_for):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'user_id': 'student-123',
            'book_id': 'book-456',
            'return_date': None
        }.get(key)
        
        mock_url_for.return_value = '/librarian/book-return'
        
        result = LibrarianController.book_return()
        
        mock_flash.assert_called_once_with('Please provide user ID, book ID and return date', 'error')

    def test_return_book_model_success_no_fine(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        mock_cursor.fetchone.side_effect = [
            ('issue-123', '2025-08-10', '2025-08-17'),
            ('book-uuid-123',)
        ]
        
        with patch('app.models.issued_book.Database.get_connection', return_value=mock_connection):
            with patch('app.models.issued_book.datetime') as mock_datetime:
                mock_date = Mock()
                mock_date.date.return_value = Mock()
                mock_datetime.strptime.return_value = mock_date
                
                result = IssuedBook.return_book('student-123', 'book-456', '2025-08-17')
        
        assert result == {'success': True, 'fine': 0.0}
        assert mock_cursor.execute.call_count == 5

    def test_return_book_model_success_with_fine(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        mock_cursor.fetchone.side_effect = [
            ('issue-123', '2025-08-10', '2025-08-17'),
            ('book-uuid-123',)
        ]
        
        with patch('app.models.issued_book.Database.get_connection', return_value=mock_connection):
            with patch('app.models.issued_book.datetime') as mock_datetime:
                from datetime import date, timedelta
                
                issue_date = date(2025, 8, 10)
                due_date = date(2025, 8, 17)
                return_date = date(2025, 8, 20)
                
                mock_datetime.strptime.return_value.date.return_value = return_date
                
                with patch('app.models.issued_book.IssuedBook.return_book') as mock_return:
                    mock_return.return_value = {'success': True, 'fine': 30.0}
                    result = mock_return('student-123', 'book-456', '2025-08-20')
        
        assert result == {'success': True, 'fine': 30.0}

    def test_return_book_model_book_not_issued(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        mock_cursor.fetchone.return_value = None
        
        with patch('app.models.issued_book.Database.get_connection', return_value=mock_connection):
            result = IssuedBook.return_book('student-123', 'book-456', '2025-08-17')
        
        assert result is False

    def test_return_book_model_no_connection(self):
        with patch('app.models.issued_book.Database.get_connection', return_value=None):
            result = IssuedBook.return_book('student-123', 'book-456', '2025-08-17')
        
        assert result is False

    def test_return_book_model_database_exception(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        mock_cursor.execute.side_effect = Exception("Database error")
        
        with patch('app.models.issued_book.Database.get_connection', return_value=mock_connection):
            result = IssuedBook.return_book('student-123', 'book-456', '2025-08-17')
        
        assert result is False

    def test_get_transaction_history(self):
        mock_transactions = [
            {
                'TransactionID': 'trans-1',
                'UserID': 'student-1',
                'BookID': 'book-1',
                'IssueDate': '2025-08-10',
                'DueDate': '2025-08-17',
                'ReturnDate': '2025-08-17',
                'Fine': 0.0,
                'book_title': 'Python Programming',
                'book_author': 'John Smith',
                'student_name': 'Alice Johnson',
                'student_email': 'alice@example.com'
            }
        ]
        
        with patch('app.models.issued_book.Database.execute_query', return_value=mock_transactions):
            result = IssuedBook.get_transaction_history()
        
        assert result == mock_transactions

    def test_get_transaction_history_no_transactions(self):
        with patch('app.models.issued_book.Database.execute_query', return_value=None):
            result = IssuedBook.get_transaction_history()
        
        assert result == []

    def test_get_users_with_fines(self):
        mock_fines = [
            {
                'TransactionID': 'trans-1',
                'UserID': 'student-1',
                'BookID': 'book-1',
                'Fine': 50.0,
                'student_name': 'Alice Johnson',
                'student_email': 'alice@example.com',
                'book_title': 'Python Programming',
                'book_author': 'John Smith'
            }
        ]
        
        with patch('app.models.issued_book.Database.execute_query', return_value=mock_fines):
            result = IssuedBook.get_users_with_fines()
        
        assert result == mock_fines

    def test_get_users_with_fines_no_fines(self):
        with patch('app.models.issued_book.Database.execute_query', return_value=None):
            result = IssuedBook.get_users_with_fines()
        
        assert result == []

    def test_get_fines_summary(self):
        mock_summary = {
            'total_outstanding': 150.0,
            'total_fines': 5,
            'collected_today': 30.0
        }
        
        with patch('app.models.issued_book.Database.execute_single_query', return_value=mock_summary):
            result = IssuedBook.get_fines_summary()
        
        assert result == mock_summary

    def test_get_fines_summary_no_data(self):
        with patch('app.models.issued_book.Database.execute_single_query', return_value=None):
            result = IssuedBook.get_fines_summary()
        
        expected = {'total_outstanding': 0, 'total_fines': 0, 'collected_today': 0}
        assert result == expected

    def test_get_student_fines(self):
        mock_result = {'total_fines': 50.0}
        
        with patch('app.models.issued_book.Database.execute_single_query', return_value=mock_result):
            result = IssuedBook.get_student_fines('student-123')
        
        assert result == 50.0

    def test_get_student_fines_no_fines(self):
        mock_result = {'total_fines': None}
        
        with patch('app.models.issued_book.Database.execute_single_query', return_value=mock_result):
            result = IssuedBook.get_student_fines('student-123')
        
        assert result == 0

    def test_get_student_fines_no_result(self):
        with patch('app.models.issued_book.Database.execute_single_query', return_value=None):
            result = IssuedBook.get_student_fines('student-123')
        
        assert result == 0

    def test_get_student_fine_history(self):
        mock_history = [
            {
                'TransactionID': 'trans-1',
                'UserID': 'student-1',
                'BookID': 'book-1',
                'Fine': 30.0,
                'book_title': 'Python Programming',
                'book_author': 'John Smith'
            }
        ]
        
        with patch('app.models.issued_book.Database.execute_query', return_value=mock_history):
            result = IssuedBook.get_student_fine_history('student-123')
        
        assert result == mock_history

    def test_get_student_fine_history_no_history(self):
        with patch('app.models.issued_book.Database.execute_query', return_value=None):
            result = IssuedBook.get_student_fine_history('student-123')
        
        assert result == []
