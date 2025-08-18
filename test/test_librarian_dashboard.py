import pytest
from unittest.mock import patch, MagicMock
from flask import session
from app import create_app
from app.controllers.librarian_controller import LibrarianController


@pytest.fixture
def app():
    app = create_app(initialize_db=False)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestLibrarianDashboard:

    def test_librarian_dashboard_loads_correctly(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'Librarian Dashboard' in response.data
        assert b'Test Librarian' in response.data

    def test_librarian_dashboard_redirects_without_login(self, client):
        response = client.get('/librarian/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_librarian_dashboard_denies_non_librarian_access(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Test Admin'
            sess['user_role'] = 'Admin'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_librarian_dashboard_denies_student_access(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Test Student'
            sess['user_role'] = 'Student'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_librarian_dashboard_displays_book_reservation_link(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Librarian User'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'Book Reservation' in response.data
        assert b'/librarian/book-reservation' in response.data

    def test_librarian_dashboard_displays_system_statistics(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Librarian User'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'Books Available' in response.data
        assert b'Books Issued' in response.data
        assert b'Books Overdue' in response.data
        assert b'Reservations' in response.data

    def test_librarian_dashboard_displays_notifications_section(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Librarian User'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'Recent Notifications' in response.data
        assert b'Library Overview' in response.data

    def test_librarian_dashboard_displays_welcome_section(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'Manage books, issues, and library operations efficiently' in response.data
        assert b'Librarian Access' in response.data

    def test_librarian_dashboard_template_rendering(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'admin-wrapper' in response.data
        assert b'Librarian' in response.data
        assert b'Logout' in response.data

    def test_librarian_dashboard_displays_available_actions(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Librarian User'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'Available Actions' in response.data

    def test_librarian_dashboard_displays_library_statistics(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Librarian User'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'Library Statistics' in response.data

    def test_librarian_dashboard_session_handling(self, client):
        response = client.get('/librarian/dashboard')
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200

    def test_librarian_dashboard_user_info_display(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'John Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/dashboard')
        assert response.status_code == 200
        assert b'John Librarian' in response.data
