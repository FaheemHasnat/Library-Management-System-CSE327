import pytest
from unittest.mock import patch, MagicMock
from flask import session
from app import create_app
from app.controllers.student_controller import StudentController


@pytest.fixture
def app():
    app = create_app(initialize_db=False)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestStudentDashboard:

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_loads_correctly(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 2
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Test Student'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        assert b'Student Dashboard' in response.data
        assert b'Test Student' in response.data

    def test_student_dashboard_redirects_without_login(self, client):
        response = client.get('/student/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_student_dashboard_denies_non_student_access(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Test Admin'
            sess['user_role'] = 'Admin'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_student_dashboard_denies_librarian_access(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_displays_account_statistics(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 1
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Student User'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        assert b'Books Issued' in response.data
        assert b'Books Available' in response.data
        assert b'Pending Fines' in response.data
        assert b'Reservations' in response.data

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_displays_notifications(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 0
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Student User'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        assert b'Notifications' in response.data
        assert b'Python Programming' in response.data
        assert b'Data Structures' in response.data

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_displays_account_balance(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 2
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Student User'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        assert b'Account Balance' in response.data
        assert b'Pending fines to pay' in response.data

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_template_rendering(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 1
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Test Student'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        assert b'admin-wrapper' in response.data
        assert b'Student' in response.data
        assert b'Logout' in response.data

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_displays_welcome_section(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 0
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Test Student'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        assert b'Access your books, manage returns, and view your library account' in response.data
        assert b'Student Access' in response.data

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_stats_data_structure(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 3
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Student User'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        data = response.get_data(as_text=True)
        assert '3' in data  # issued books
        assert '1247' in data  # available books
        assert '0.00' in data  # pending fines

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_reservation_count_display(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 2
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Student User'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        mock_reservation_count.assert_called_once_with(3)

    @patch('app.models.book.Book.get_user_reservation_count')
    def test_student_dashboard_user_info_display(self, mock_reservation_count, client):
        mock_reservation_count.return_value = 1
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Jane Student'
            sess['user_role'] = 'Student'
        
        response = client.get('/student/dashboard')
        assert response.status_code == 200
        assert b'Jane Student' in response.data

    def test_student_dashboard_session_handling(self, client):
        response = client.get('/student/dashboard')
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_role'] = 'Student'
        
        with patch('app.models.book.Book.get_user_reservation_count', return_value=0):
            response = client.get('/student/dashboard')
            assert response.status_code == 200
