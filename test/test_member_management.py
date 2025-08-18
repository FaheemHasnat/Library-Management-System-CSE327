import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.controllers.admin_controller import AdminController
from app.models.user import User


class TestMemberManagement:
    
    @pytest.fixture
    def mock_session(self):
        with patch('app.controllers.admin_controller.session') as mock:
            mock.get.side_effect = lambda key, default=None: {
                'user_id': 'admin-001',
                'user_role': 'Admin',
                'user_name': 'Test Admin'
            }.get(key, default)
            yield mock
    
    @pytest.fixture
    def mock_database(self):
        with patch('app.controllers.admin_controller.Database') as mock:
            yield mock
    
    @pytest.fixture
    def mock_user_model(self):
        with patch('app.controllers.admin_controller.User') as mock:
            yield mock
    
    @pytest.fixture
    def mock_flash(self):
        with patch('app.controllers.admin_controller.flash') as mock:
            yield mock
    
    @pytest.fixture
    def mock_redirect(self):
        with patch('app.controllers.admin_controller.redirect') as mock:
            yield mock
    
    @pytest.fixture
    def mock_render_template(self):
        with patch('app.controllers.admin_controller.render_template') as mock:
            yield mock

    def test_get_member_count_success(self, mock_database):
        mock_database.execute_single_query.return_value = {'count': 25}
        
        result = AdminController.get_member_count()
        
        assert result == 25
        mock_database.execute_single_query.assert_called_once_with("SELECT COUNT(*) as count FROM users")
    
    def test_get_member_count_no_result(self, mock_database):
        mock_database.execute_single_query.return_value = None
        
        result = AdminController.get_member_count()
        
        assert result == 0
    
    def test_get_member_count_by_role_success(self, mock_database):
        mock_database.execute_single_query.return_value = {'count': 10}
        
        result = AdminController.get_member_count_by_role('Student')
        
        assert result == 10
        mock_database.execute_single_query.assert_called_once_with("SELECT COUNT(*) as count FROM users WHERE Role = %s", ('Student',))
    
    def test_get_member_count_by_role_no_result(self, mock_database):
        mock_database.execute_single_query.return_value = None
        
        result = AdminController.get_member_count_by_role('Librarian')
        
        assert result == 0

    @patch('app.controllers.admin_controller.request')
    def test_member_management_success(self, mock_request, mock_session, mock_database, mock_render_template):
        mock_database.execute_single_query.side_effect = [
            {'count': 25},
            {'count': 15},
            {'count': 8},
            {'count': 2}
        ]
        
        result = AdminController.member_management()
        
        mock_render_template.assert_called_once_with(
            'admin/member_management.html',
            user_name='Test Admin',
            total_members=25,
            student_count=15,
            librarian_count=8,
            admin_count=2
        )

    @patch('app.controllers.admin_controller.request')
    def test_add_member_get_request(self, mock_request, mock_session, mock_render_template):
        mock_request.method = 'GET'
        
        result = AdminController.add_member()
        
        mock_render_template.assert_called_once_with('admin/add_member.html', user_name='Test Admin')

    @patch('app.controllers.admin_controller.request')
    @patch('app.controllers.admin_controller.url_for')
    def test_add_member_post_success(self, mock_url_for, mock_request, mock_session, mock_user_model, mock_flash, mock_redirect):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(key)
        
        mock_user_model.get_by_email.return_value = None
        mock_user_model.create_user.return_value = Mock()
        mock_url_for.return_value = '/admin/member-management'
        
        result = AdminController.add_member()
        
        mock_user_model.create_user.assert_called_once_with('John Doe', 'john@example.com', 'password123', 'Student')
        mock_flash.assert_called_once_with('Member John Doe added successfully!', 'success')
        mock_redirect.assert_called_once()

    @patch('app.controllers.admin_controller.request')
    def test_add_member_missing_fields(self, mock_request, mock_session, mock_flash, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'name': 'John Doe',
            'email': '',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(key)
        
        result = AdminController.add_member()
        
        mock_flash.assert_called_once_with('Please fill in all fields', 'error')
        mock_render_template.assert_called_once_with('admin/add_member.html', user_name='Test Admin')

    @patch('app.controllers.admin_controller.request')
    def test_add_member_invalid_role(self, mock_request, mock_session, mock_flash, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'InvalidRole',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(key)
        
        result = AdminController.add_member()
        
        mock_flash.assert_called_once_with('Invalid role selected', 'error')

    @patch('app.controllers.admin_controller.request')
    def test_add_member_password_mismatch(self, mock_request, mock_session, mock_flash, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        }.get(key)
        
        result = AdminController.add_member()
        
        mock_flash.assert_called_once_with('Passwords do not match', 'error')

    @patch('app.controllers.admin_controller.request')
    def test_add_member_short_password(self, mock_request, mock_session, mock_flash, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'Student',
            'password': '123',
            'confirm_password': '123'
        }.get(key)
        
        result = AdminController.add_member()
        
        mock_flash.assert_called_once_with('Password must be at least 6 characters long', 'error')

    @patch('app.controllers.admin_controller.request')
    def test_add_member_email_exists(self, mock_request, mock_session, mock_user_model, mock_flash, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'Student',
            'password': 'password123',
            'confirm_password': 'password123'
        }.get(key)
        
        mock_user_model.get_by_email.return_value = Mock()
        
        result = AdminController.add_member()
        
        mock_flash.assert_called_once_with('Email already exists', 'error')

    def test_view_all_members_success(self, mock_session, mock_database, mock_render_template):
        mock_members = [
            {'UserID': '1', 'Name': 'John Doe', 'Email': 'john@example.com', 'Role': 'Student'},
            {'UserID': '2', 'Name': 'Jane Smith', 'Email': 'jane@example.com', 'Role': 'Librarian'}
        ]
        mock_database.execute_query.return_value = mock_members
        
        result = AdminController.view_all_members()
        
        mock_render_template.assert_called_once_with(
            'admin/view_all_members.html',
            user_name='Test Admin',
            members=mock_members
        )

    def test_view_all_members_no_members(self, mock_session, mock_database, mock_render_template):
        mock_database.execute_query.return_value = None
        
        result = AdminController.view_all_members()
        
        mock_render_template.assert_called_once_with(
            'admin/view_all_members.html',
            user_name='Test Admin',
            members=[]
        )

    @patch('app.controllers.admin_controller.request')
    def test_edit_member_get_request(self, mock_request, mock_session, mock_render_template):
        mock_request.method = 'GET'
        
        result = AdminController.edit_member()
        
        mock_render_template.assert_called_once_with(
            'admin/edit_member.html',
            user_name='Test Admin',
            member=None
        )

    @patch('app.controllers.admin_controller.request')
    def test_edit_member_find_by_email(self, mock_request, mock_session, mock_user_model, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'action': 'find',
            'email': 'john@example.com'
        }.get(key)
        
        mock_member = Mock()
        mock_user_model.get_by_email.return_value = mock_member
        
        result = AdminController.edit_member()
        
        mock_render_template.assert_called_once_with(
            'admin/edit_member.html',
            user_name='Test Admin',
            member=mock_member
        )

    @patch('app.controllers.admin_controller.request')
    def test_edit_member_email_not_found(self, mock_request, mock_session, mock_user_model, mock_flash, mock_render_template):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'action': 'find',
            'email': 'notfound@example.com'
        }.get(key)
        
        mock_user_model.get_by_email.return_value = None
        
        result = AdminController.edit_member()
        
        mock_flash.assert_called_once_with('Member not found with this email', 'error')

    @patch('app.controllers.admin_controller.request')
    @patch('app.controllers.admin_controller.url_for')
    def test_update_member_success(self, mock_url_for, mock_request, mock_session, mock_user_model, mock_flash, mock_redirect):
        mock_request.method = 'POST'
        mock_request.form.get.side_effect = lambda key: {
            'action': 'update',
            'user_id': 'user-123',
            'name': 'Updated Name',
            'role': 'Student',
            'new_password': 'newpassword123'
        }.get(key)
        
        mock_current_member = Mock()
        mock_current_member.email = 'user@example.com'
        mock_user_model.get_by_id.return_value = mock_current_member
        
        with patch.object(AdminController, 'update_member', return_value=True):
            result = AdminController.edit_member()
        
        mock_flash.assert_called_once_with('Member updated successfully!', 'success')

    def test_delete_member_by_user_id_success(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 1
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        with patch('app.controllers.admin_controller.Database.get_connection', return_value=mock_connection):
            result = AdminController.delete_member_by_user_id('user-123')
        
        assert result is True
        mock_cursor.execute.assert_called_once_with("DELETE FROM users WHERE UserID = %s", ('user-123',))

    def test_delete_member_by_user_id_no_rows_affected(self):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 0
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        with patch('app.controllers.admin_controller.Database.get_connection', return_value=mock_connection):
            result = AdminController.delete_member_by_user_id('user-123')
        
        assert result is False

    def test_delete_member_by_user_id_database_error(self):
        with patch('app.controllers.admin_controller.Database.get_connection', return_value=None):
            result = AdminController.delete_member_by_user_id('user-123')
        
        assert result is False

    @patch('app.controllers.admin_controller.request')
    @patch('app.controllers.admin_controller.url_for')
    def test_delete_member_by_id_success(self, mock_url_for, mock_request, mock_session, mock_flash, mock_redirect):
        with patch.object(AdminController, 'delete_member_by_user_id', return_value=True):
            result = AdminController.delete_member_by_id('user-123')
        
        mock_flash.assert_called_once_with('Member deleted successfully!', 'success')

    @patch('app.controllers.admin_controller.request')
    @patch('app.controllers.admin_controller.url_for')
    def test_delete_member_by_id_failure(self, mock_url_for, mock_request, mock_session, mock_flash, mock_redirect):
        with patch.object(AdminController, 'delete_member_by_user_id', return_value=False):
            result = AdminController.delete_member_by_id('user-123')
        
        mock_flash.assert_called_once_with('Error deleting member. Please try again.', 'error')

    def test_check_admin_access_valid_admin(self, mock_session):
        result = AdminController.check_admin_access()
        
        assert result is None

    def test_check_admin_access_no_session(self, mock_flash, mock_redirect):
        with patch('app.controllers.admin_controller.session') as mock_session:
            mock_session.get.side_effect = lambda key, default=None: {}.get(key, default)
            
            result = AdminController.check_admin_access()
        
        mock_flash.assert_called_once_with('Access denied', 'error')

    def test_check_admin_access_wrong_role(self, mock_flash, mock_redirect):
        with patch('app.controllers.admin_controller.session') as mock_session:
            mock_session.get.side_effect = lambda key, default=None: {
                'user_id': 'user-001',
                'user_role': 'Student'
            }.get(key, default)
            
            result = AdminController.check_admin_access()
        
        mock_flash.assert_called_once_with('Access denied', 'error')
