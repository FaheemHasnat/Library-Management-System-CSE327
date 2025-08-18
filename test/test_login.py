import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.auth_controller import AuthController
from app.models.user import User


class TestLogin:
    
    @pytest.fixture
    def mock_flask_session(self):
        with patch('app.controllers.auth_controller.session', {}) as mock_session:
            yield mock_session
    
    @pytest.fixture
    def mock_flask_request(self):
        with patch('app.controllers.auth_controller.request') as mock_request:
            yield mock_request
    
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
    
    def test_login_get_request(self, mock_flask_request, mock_render_template):
        mock_flask_request.method = 'GET'
        
        result = AuthController.login()
        
        mock_render_template.assert_called_once_with('auth/login.html')
    
    def test_login_post_missing_email(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: '' if x == 'email' else 'password123'
        
        result = AuthController.login()
        
        mock_flask_flash.assert_called_with('Please enter both email and password', 'error')
        mock_render_template.assert_called_with('auth/login.html')
    
    def test_login_post_missing_password(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: 'user@email.com' if x == 'email' else ''
        
        result = AuthController.login()
        
        mock_flask_flash.assert_called_with('Please enter both email and password', 'error')
        mock_render_template.assert_called_with('auth/login.html')
    
    @patch('app.controllers.auth_controller.User.authenticate')
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    def test_login_invalid_credentials(self, mock_init, mock_authenticate, mock_flask_request, 
                                     mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: 'user@email.com' if x == 'email' else 'wrongpass'
        mock_authenticate.return_value = None
        
        result = AuthController.login()
        
        mock_flask_flash.assert_called_with('Invalid email or password', 'error')
        mock_render_template.assert_called_with('auth/login.html')
    
    @patch('app.controllers.auth_controller.User.authenticate')
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    @patch('app.controllers.auth_controller.url_for')
    def test_login_admin_success(self, mock_url_for, mock_init, mock_authenticate, 
                                mock_flask_request, mock_flask_session, mock_flask_flash, 
                                mock_flask_redirect):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: 'admin@lms.com' if x == 'email' else 'admin123'
        
        mock_user = MagicMock()
        mock_user.user_id = 'admin-001'
        mock_user.name = 'Admin User'
        mock_user.email = 'admin@lms.com'
        mock_user.role = 'Admin'
        mock_authenticate.return_value = mock_user
        
        mock_url_for.return_value = '/admin/dashboard'
        
        result = AuthController.login()
        
        assert mock_flask_session['user_id'] == 'admin-001'
        assert mock_flask_session['user_role'] == 'Admin'
        mock_flask_flash.assert_called_with('Welcome back, Admin User!', 'success')
        mock_flask_redirect.assert_called_once()
    
    @patch('app.controllers.auth_controller.User.authenticate')
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    @patch('app.controllers.auth_controller.url_for')
    def test_login_librarian_success(self, mock_url_for, mock_init, mock_authenticate, 
                                   mock_flask_request, mock_flask_session, mock_flask_flash, 
                                   mock_flask_redirect):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: 'librarian@lms.com' if x == 'email' else 'lib123'
        
        mock_user = MagicMock()
        mock_user.user_id = 'lib-001'
        mock_user.name = 'Librarian User'
        mock_user.email = 'librarian@lms.com'
        mock_user.role = 'Librarian'
        mock_authenticate.return_value = mock_user
        
        mock_url_for.return_value = '/librarian/dashboard'
        
        result = AuthController.login()
        
        assert mock_flask_session['user_id'] == 'lib-001'
        assert mock_flask_session['user_role'] == 'Librarian'
        mock_flask_flash.assert_called_with('Welcome back, Librarian User!', 'success')
    
    @patch('app.controllers.auth_controller.User.authenticate')
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    @patch('app.controllers.auth_controller.url_for')
    def test_login_student_success(self, mock_url_for, mock_init, mock_authenticate, 
                                 mock_flask_request, mock_flask_session, mock_flask_flash, 
                                 mock_flask_redirect):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: 'student@lms.com' if x == 'email' else 'student123'
        
        mock_user = MagicMock()
        mock_user.user_id = 'student-001'
        mock_user.name = 'Student User'
        mock_user.email = 'student@lms.com'
        mock_user.role = 'Student'
        mock_authenticate.return_value = mock_user
        
        mock_url_for.return_value = '/student/dashboard'
        
        result = AuthController.login()
        
        assert mock_flask_session['user_id'] == 'student-001'
        assert mock_flask_session['user_role'] == 'Student'
        mock_flask_flash.assert_called_with('Welcome back, Student User!', 'success')
    
    def test_login_empty_form_data(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.return_value = None
        
        result = AuthController.login()
        
        mock_flask_flash.assert_called_with('Please enter both email and password', 'error')
        mock_render_template.assert_called_with('auth/login.html')
    
    @patch('app.controllers.auth_controller.User.authenticate')
    @patch('app.controllers.auth_controller.User.initialize_sample_data')
    def test_login_database_error(self, mock_init, mock_authenticate, mock_flask_request, 
                                mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: 'user@email.com' if x == 'email' else 'password123'
        mock_authenticate.side_effect = Exception('Database connection error')
        
        with pytest.raises(Exception):
            AuthController.login()
