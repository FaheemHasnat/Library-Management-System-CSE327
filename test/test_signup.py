import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.auth_controller import AuthController
from app.models.user import User


class TestSignup:
    
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
    
    @pytest.fixture
    def mock_url_for(self):
        with patch('app.controllers.auth_controller.url_for') as mock_url:
            yield mock_url
    
    def test_signup_get_request(self, mock_flask_request, mock_render_template):
        mock_flask_request.method = 'GET'
        
        result = AuthController.signup()
        
        mock_render_template.assert_called_once_with('auth/signup.html')
    
    def test_signup_missing_fields(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': '',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(x, '')
        
        result = AuthController.signup()
        
        mock_flask_flash.assert_called_with('Please fill in all fields', 'error')
        mock_render_template.assert_called_with('auth/signup.html')
    
    def test_signup_invalid_role(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': 'john@email.com',
            'role': 'Admin',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(x, '')
        
        result = AuthController.signup()
        
        mock_flask_flash.assert_called_with('Invalid role selected', 'error')
        mock_render_template.assert_called_with('auth/signup.html')
    
    def test_signup_password_mismatch(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': 'john@email.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'different123'
        }.get(x, '')
        
        result = AuthController.signup()
        
        mock_flask_flash.assert_called_with('Passwords do not match', 'error')
        mock_render_template.assert_called_with('auth/signup.html')
    
    def test_signup_short_password(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': 'john@email.com',
            'role': 'Student',
            'password': '123',
            'confirm_password': '123'
        }.get(x, '')
        
        result = AuthController.signup()
        
        mock_flask_flash.assert_called_with('Password must be at least 6 characters long', 'error')
        mock_render_template.assert_called_with('auth/signup.html')
    
    @patch('app.controllers.auth_controller.User.get_by_email')
    def test_signup_existing_email(self, mock_get_by_email, mock_flask_request, 
                                 mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': 'existing@email.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(x, '')
        
        mock_existing_user = MagicMock()
        mock_get_by_email.return_value = mock_existing_user
        
        result = AuthController.signup()
        
        mock_flask_flash.assert_called_with('Email already exists', 'error')
        mock_render_template.assert_called_with('auth/signup.html')
    
    @patch('app.controllers.auth_controller.User.get_by_email')
    @patch('app.controllers.auth_controller.User.create_user')
    def test_signup_success(self, mock_create_user, mock_get_by_email, mock_flask_request, 
                          mock_flask_flash, mock_flask_redirect, mock_url_for):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': 'new@email.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(x, '')
        
        mock_get_by_email.return_value = None
        mock_new_user = MagicMock()
        mock_create_user.return_value = mock_new_user
        mock_url_for.return_value = '/login'
        
        result = AuthController.signup()
        
        mock_create_user.assert_called_once_with('John Doe', 'new@email.com', 'password123', 'Student')
        mock_flask_flash.assert_called_with('Account created successfully! Please login.', 'success')
        mock_flask_redirect.assert_called_once()
    
    @patch('app.controllers.auth_controller.User.get_by_email')
    @patch('app.controllers.auth_controller.User.create_user')
    def test_signup_create_user_fails(self, mock_create_user, mock_get_by_email, mock_flask_request, 
                                    mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': 'new@email.com',
            'role': 'Librarian',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(x, '')
        
        mock_get_by_email.return_value = None
        mock_create_user.return_value = None
        
        result = AuthController.signup()
        
        mock_flask_flash.assert_called_with('Error creating account. Please try again.', 'error')
        mock_render_template.assert_called_with('auth/signup.html')
    
    def test_signup_all_fields_none(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.return_value = None
        
        result = AuthController.signup()
        
        mock_flask_flash.assert_called_with('Please fill in all fields', 'error')
        mock_render_template.assert_called_with('auth/signup.html')
    
    def test_signup_valid_roles(self, mock_flask_request, mock_flask_flash, mock_render_template):
        for role in ['Student', 'Librarian']:
            mock_flask_request.method = 'POST'
            mock_flask_request.form.get.side_effect = lambda x: {
                'name': 'John Doe',
                'email': 'john@email.com',
                'role': role,
                'password': 'password123',
                'confirm_password': 'different123'
            }.get(x, '')
            
            result = AuthController.signup()
            
            mock_flask_flash.assert_called_with('Passwords do not match', 'error')
    
    def test_signup_edge_case_password_length(self, mock_flask_request, mock_flask_flash, mock_render_template):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': 'john@email.com',
            'role': 'Student',
            'password': '12345',
            'confirm_password': '12345'
        }.get(x, '')
        
        result = AuthController.signup()
        
        mock_flask_flash.assert_called_with('Password must be at least 6 characters long', 'error')
        mock_render_template.assert_called_with('auth/signup.html')
    
    @patch('app.controllers.auth_controller.User.get_by_email')
    def test_signup_database_error(self, mock_get_by_email, mock_flask_request):
        mock_flask_request.method = 'POST'
        mock_flask_request.form.get.side_effect = lambda x: {
            'name': 'John Doe',
            'email': 'new@email.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(x, '')
        
        mock_get_by_email.side_effect = Exception('Database connection error')
        
        with pytest.raises(Exception):
            AuthController.signup()
