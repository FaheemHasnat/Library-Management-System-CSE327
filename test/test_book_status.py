import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.auth_controller import AuthController
from app.models.user import User


class TestBookStatus:
    
    @pytest.fixture
    def mock_flask_session(self):
        with patch('app.controllers.auth_controller.session', {}) as mock_session:
            yield mock_session
    
    @pytest.fixture
    def mock_flask_flash(self):
        with patch('app.controllers.auth_controller.flash') as mock_flash:
            yield mock_flash
    
    @pytest.fixture
    def mock_flask_redirect(self):
        with patch('app.controllers.auth_controller.redirect') as mock_redirect:
            yield mock_redirect
    
    @pytest.fixture
    def mock_render_template(self):
        with patch('app.controllers.auth_controller.render_template') as mock_template:
            yield mock_template
    
    @pytest.fixture
    def mock_url_for(self):
        with patch('app.controllers.auth_controller.url_for') as mock_url:
            yield mock_url
    
    @pytest.fixture
    def sample_books(self):
        return [
            {
                'title': 'The Art of Computer Programming',
                'author': 'Donald Knuth',
                'subject': 'Computer Science',
                'isbn': '978-0-13-110362-7',
                'status': 'Available'
            },
            {
                'title': 'Introduction to Algorithms',
                'author': 'Thomas Cormen',
                'subject': 'Computer Science',
                'isbn': '978-0-262-03384-8',
                'status': 'Borrowed'
            },
            {
                'title': 'Clean Code',
                'author': 'Robert Martin',
                'subject': 'Software Engineering',
                'isbn': '978-0-13-597269-4',
                'status': 'Reserved'
            }
        ]


class TestAdminBookStatus(TestBookStatus):
    
    def test_admin_book_status_no_session(self, mock_flask_session, mock_flask_flash, 
                                        mock_flask_redirect, mock_url_for):
        mock_flask_session.get.return_value = None
        mock_url_for.return_value = '/login'
        
        result = AuthController.admin_book_status()
        
        mock_flask_flash.assert_called_with('Access denied', 'error')
        mock_flask_redirect.assert_called_once()
    
    def test_admin_book_status_wrong_role(self, mock_flask_session, mock_flask_flash, 
                                        mock_flask_redirect, mock_url_for):
        mock_flask_session.__contains__.return_value = True
        mock_flask_session.get.side_effect = lambda x: 'Student' if x == 'user_role' else 'user123'
        mock_url_for.return_value = '/login'
        
        result = AuthController.admin_book_status()
        
        mock_flask_flash.assert_called_with('Access denied', 'error')
        mock_flask_redirect.assert_called_once()
    
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    @patch('app.controllers.auth_controller.User.get_all_books')
    def test_admin_book_status_success(self, mock_get_books, mock_init, mock_flask_session, 
                                     mock_render_template, sample_books):
        mock_flask_session.__contains__.return_value = True
        mock_flask_session.get.side_effect = lambda x: {
            'user_role': 'Admin',
            'user_name': 'Admin User'
        }.get(x)
        
        mock_get_books.return_value = sample_books
        
        result = AuthController.admin_book_status()
        
        mock_init.assert_called_once()
        mock_get_books.assert_called_once()
        mock_render_template.assert_called_with('admin/book_status.html', 
                                              user_name='Admin User', 
                                              books=sample_books)
    
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    @patch('app.controllers.auth_controller.User.get_all_books')
    def test_admin_book_status_empty_books(self, mock_get_books, mock_init, mock_flask_session, 
                                         mock_render_template):
        mock_flask_session.__contains__.return_value = True
        mock_flask_session.get.side_effect = lambda x: {
            'user_role': 'Admin',
            'user_name': 'Admin User'
        }.get(x)
        
        mock_get_books.return_value = []
        
        result = AuthController.admin_book_status()
        
        mock_render_template.assert_called_with('admin/book_status.html', 
                                              user_name='Admin User', 
                                              books=[])


class TestLibrarianBookStatus(TestBookStatus):
    
    def test_librarian_book_status_no_session(self, mock_flask_session, mock_flask_flash, 
                                            mock_flask_redirect, mock_url_for):
        mock_flask_session.get.return_value = None
        mock_url_for.return_value = '/login'
        
        result = AuthController.librarian_book_status()
        
        mock_flask_flash.assert_called_with('Access denied', 'error')
        mock_flask_redirect.assert_called_once()
    
    def test_librarian_book_status_wrong_role(self, mock_flask_session, mock_flask_flash, 
                                            mock_flask_redirect, mock_url_for):
        mock_flask_session.__contains__.return_value = True
        mock_flask_session.get.side_effect = lambda x: 'Admin' if x == 'user_role' else 'user123'
        mock_url_for.return_value = '/login'
        
        result = AuthController.librarian_book_status()
        
        mock_flask_flash.assert_called_with('Access denied', 'error')
        mock_flask_redirect.assert_called_once()
    
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    @patch('app.controllers.auth_controller.User.get_all_books')
    def test_librarian_book_status_success(self, mock_get_books, mock_init, mock_flask_session, 
                                         mock_render_template, sample_books):
        mock_flask_session.__contains__.return_value = True
        mock_flask_session.get.side_effect = lambda x: {
            'user_role': 'Librarian',
            'user_name': 'Librarian User'
        }.get(x)
        
        mock_get_books.return_value = sample_books
        
        result = AuthController.librarian_book_status()
        
        mock_init.assert_called_once()
        mock_get_books.assert_called_once()
        mock_render_template.assert_called_with('librarian/book_status.html', 
                                              user_name='Librarian User', 
                                              books=sample_books)


class TestStudentBookStatus(TestBookStatus):
    
    def test_student_book_status_no_session(self, mock_flask_session, mock_flask_flash, 
                                          mock_flask_redirect, mock_url_for):
        mock_flask_session.get.return_value = None
        mock_url_for.return_value = '/login'
        
        result = AuthController.student_book_status()
        
        mock_flask_flash.assert_called_with('Access denied', 'error')
        mock_flask_redirect.assert_called_once()
    
    def test_student_book_status_wrong_role(self, mock_flask_session, mock_flask_flash, 
                                          mock_flask_redirect, mock_url_for):
        mock_flask_session.__contains__.return_value = True
        mock_flask_session.get.side_effect = lambda x: 'Librarian' if x == 'user_role' else 'user123'
        mock_url_for.return_value = '/login'
        
        result = AuthController.student_book_status()
        
        mock_flask_flash.assert_called_with('Access denied', 'error')
        mock_flask_redirect.assert_called_once()
    
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    @patch('app.controllers.auth_controller.User.get_all_books')
    def test_student_book_status_success(self, mock_get_books, mock_init, mock_flask_session, 
                                       mock_render_template, sample_books):
        mock_flask_session.__contains__.return_value = True
        mock_flask_session.get.side_effect = lambda x: {
            'user_role': 'Student',
            'user_name': 'Student User'
        }.get(x)
        
        mock_get_books.return_value = sample_books
        
        result = AuthController.student_book_status()
        
        mock_init.assert_called_once()
        mock_get_books.assert_called_once()
        mock_render_template.assert_called_with('student/book_status.html', 
                                              user_name='Student User', 
                                              books=sample_books)


class TestBookDataModel:
    
    @patch('app.models.user.Database.execute_query')
    @patch('app.models.user.User.initialize_sample_books')
    def test_get_all_books_success(self, mock_init, mock_execute_query):
        mock_books_data = [
            {
                'title': 'Test Book 1',
                'author': 'Test Author 1',
                'subject': 'Test Subject',
                'isbn': '123456789',
                'status': 'Available'
            },
            {
                'title': 'Test Book 2',
                'author': 'Test Author 2',
                'subject': 'Test Subject',
                'isbn': '987654321',
                'status': 'Borrowed'
            }
        ]
        mock_execute_query.return_value = mock_books_data
        
        result = User.get_all_books()
        
        assert len(result) == 2
        assert result[0]['title'] == 'Test Book 1'
        assert result[1]['status'] == 'Borrowed'
        mock_init.assert_called_once()
    
    @patch('app.models.user.Database.execute_query')
    @patch('app.models.user.User.initialize_sample_books')
    def test_get_all_books_empty_result(self, mock_init, mock_execute_query):
        mock_execute_query.return_value = []
        
        result = User.get_all_books()
        
        assert result == []
        mock_init.assert_called_once()
    
    @patch('app.models.user.Database.execute_query')
    @patch('app.models.user.User.initialize_sample_books')
    def test_get_all_books_none_result(self, mock_init, mock_execute_query):
        mock_execute_query.return_value = None
        
        result = User.get_all_books()
        
        assert result == []
        mock_init.assert_called_once()
    
    @patch('app.models.user.Database.execute_query')
    @patch('app.models.user.User.initialize_sample_books')
    def test_get_all_books_database_error(self, mock_init, mock_execute_query):
        mock_execute_query.side_effect = Exception('Database connection failed')
        
        result = User.get_all_books()
        
        assert result == []
    
    @patch('app.models.user.Database.execute_query')
    @patch('app.models.user.User.initialize_sample_books')
    def test_get_all_books_missing_fields(self, mock_init, mock_execute_query):
        mock_books_data = [
            {
                'title': 'Test Book',
                'author': 'Test Author'
            }
        ]
        mock_execute_query.return_value = mock_books_data
        
        result = User.get_all_books()
        
        assert len(result) == 1
        assert result[0]['title'] == 'Test Book'
        assert result[0]['subject'] == ''
        assert result[0]['isbn'] == ''
        assert result[0]['status'] == ''
    
    def test_book_status_filtering(self):
        books = [
            {'title': 'Book 1', 'status': 'Available'},
            {'title': 'Book 2', 'status': 'Borrowed'},
            {'title': 'Book 3', 'status': 'Reserved'},
            {'title': 'Book 4', 'status': 'Available'}
        ]
        
        available_books = [book for book in books if book['status'] == 'Available']
        borrowed_books = [book for book in books if book['status'] == 'Borrowed']
        reserved_books = [book for book in books if book['status'] == 'Reserved']
        
        assert len(available_books) == 2
        assert len(borrowed_books) == 1
        assert len(reserved_books) == 1
    
    def test_book_status_statistics(self):
        books = [
            {'status': 'Available'},
            {'status': 'Available'},
            {'status': 'Borrowed'},
            {'status': 'Reserved'}
        ]
        
        total_books = len(books)
        available_count = len([b for b in books if b['status'] == 'Available'])
        borrowed_count = len([b for b in books if b['status'] == 'Borrowed'])
        reserved_count = len([b for b in books if b['status'] == 'Reserved'])
        
        assert total_books == 4
        assert available_count == 2
        assert borrowed_count == 1
        assert reserved_count == 1
        
        if total_books > 0:
            availability_percentage = (available_count / total_books) * 100
            assert availability_percentage == 50.0
