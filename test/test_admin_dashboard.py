import pytest
from unittest.mock import patch, MagicMock
from flask import session
from app import create_app
from app.controllers.admin_controller import AdminController


@pytest.fixture
def app():
    app = create_app(initialize_db=False)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestAdminDashboard:

    def test_admin_dashboard_loads_correctly(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Test Admin'
            sess['user_role'] = 'Admin'
        
        response = client.get('/admin/dashboard')
        assert response.status_code == 200
        assert b'Admin Dashboard' in response.data
        assert b'Test Admin' in response.data

    def test_admin_dashboard_redirects_without_login(self, client):
        response = client.get('/admin/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_admin_dashboard_denies_non_admin_access(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Student'
            sess['user_role'] = 'Student'
        
        response = client.get('/admin/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_admin_dashboard_denies_librarian_access(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 3
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/admin/dashboard')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_admin_dashboard_displays_system_statistics(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Admin User'
            sess['user_role'] = 'Admin'
        
        response = client.get('/admin/dashboard')
        assert response.status_code == 200
        assert b'Total Books' in response.data
        assert b'Total Members' in response.data
        assert b'Books Issued' in response.data
        assert b'Reservations' in response.data

    def test_admin_dashboard_displays_notifications_section(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Admin User'
            sess['user_role'] = 'Admin'
        
        response = client.get('/admin/dashboard')
        assert response.status_code == 200
        assert b'Recent Notifications' in response.data
        assert b'Total Fines Collected' in response.data

    def test_admin_check_access_allows_admin(self):
        with patch('flask.session', {'user_id': 1, 'user_role': 'Admin'}):
            result = AdminController.check_admin_access()
            assert result is None

    def test_admin_check_access_denies_non_admin(self):
        with patch('flask.session', {'user_id': 2, 'user_role': 'Student'}):
            with patch('flask.flash') as mock_flash:
                with patch('flask.redirect') as mock_redirect:
                    AdminController.check_admin_access()
                    mock_flash.assert_called_once_with('Access denied', 'error')

    def test_admin_check_access_denies_no_session(self):
        with patch('flask.session', {}):
            with patch('flask.flash') as mock_flash:
                with patch('flask.redirect') as mock_redirect:
                    AdminController.check_admin_access()
                    mock_flash.assert_called_once_with('Access denied', 'error')

    def test_admin_dashboard_template_rendering(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Test Admin'
            sess['user_role'] = 'Admin'
        
        response = client.get('/admin/dashboard')
        assert response.status_code == 200
        assert b'admin-wrapper' in response.data
        assert b'Administrator' in response.data
        assert b'Logout' in response.data

    def test_admin_dashboard_displays_welcome_section(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Test Admin'
            sess['user_role'] = 'Admin'
        
        response = client.get('/admin/dashboard')
        assert response.status_code == 200
        assert b'Complete control over your library management system' in response.data
        assert b'Administrator Access' in response.data
