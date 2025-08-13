<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
from app.utils.lms_db import DatabaseConnection
import hashlib
import logging
import uuid


class UserModel:
    
    @staticmethod
    def authenticate_user(email, password):
        try:
            db = DatabaseConnection()
            
            query = "SELECT UserID, Name, Email, Password, Role FROM users WHERE Email = %s"
            user = db.execute_query(query, (email,), fetch_one=True)
            
            if user and UserModel._verify_password(password, user['Password']):
                return {
                    'UserID': user['UserID'],
                    'Name': user['Name'],
                    'Email': user['Email'],
                    'Role': user['Role']
                }
            
            return None
            
<<<<<<< HEAD
=======
=======
"""
User Model for Library Management System
Handles user authentication, registration, and user-related database operations
"""

import hashlib
import uuid
from datetime import datetime
from app.utils.lms_db import db
import logging


class UserModel:
    """Model class for user operations"""
    
    @staticmethod
    def hash_password(password):
        """
        Hash password using SHA-256
        
        Args:
            password (str): Plain text password
        
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_user_id():
        """
        Generate unique user ID
        
        Returns:
            str: Unique user ID
        """
        return str(uuid.uuid4())
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate user credentials
        
        Args:
            email (str): User email
            password (str): Plain text password
        
        Returns:
            dict/None: User data if authentication successful, None otherwise
        """
        try:
            hashed_password = UserModel.hash_password(password)
            
            query = """
                SELECT UserID, Name, Email, Role 
                FROM users 
                WHERE Email = %s AND Password = %s
            """
            
            user = db.execute_query(query, (email, hashed_password), fetch_one=True)
            
            if user:
                logging.info(f"User authenticated successfully: {email}")
                return user
            else:
                logging.warning(f"Authentication failed for email: {email}")
                return None
                
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return None
    
    @staticmethod
    def register_user(name, email, password, role='Student'):
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
        try:
            db = DatabaseConnection()
            
            # Check if email already exists
            check_query = "SELECT UserID FROM users WHERE Email = %s"
            existing_user = db.execute_query(check_query, (email,), fetch_one=True)
            
            if existing_user:
<<<<<<< HEAD
=======
=======
        """
        Register a new user
        
        Args:
            name (str): User name
            email (str): User email
            password (str): Plain text password
            role (str): User role (Student, Librarian, Admin)
        
        Returns:
            dict: Result with success status and message
        """
        try:
            # Check if email already exists
            if UserModel.email_exists(email):
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                return {
                    'success': False,
                    'message': 'Email already registered'
                }
            
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            # Create new user
            user_id = str(uuid.uuid4())
            hashed_password = UserModel._hash_password(password)
            
            insert_query = """
<<<<<<< HEAD
=======
=======
            # Generate user ID and hash password
            user_id = UserModel.generate_user_id()
            hashed_password = UserModel.hash_password(password)
            
            # Insert new user
            query = """
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                INSERT INTO users (UserID, Name, Email, Password, Role)
                VALUES (%s, %s, %s, %s, %s)
            """
            
<<<<<<< HEAD
            result = db.execute_query(insert_query, (user_id, name, email, hashed_password, role))
            
            if result:
=======
<<<<<<< HEAD
            result = db.execute_query(insert_query, (user_id, name, email, hashed_password, role))
            
            if result:
=======
            result = db.execute_query(
                query, 
                (user_id, name, email, hashed_password, role),
                fetch_all=False
            )
            
            if result:
                logging.info(f"User registered successfully: {email}")
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                return {
                    'success': True,
                    'message': 'User registered successfully',
                    'user_id': user_id
                }
            else:
                return {
                    'success': False,
<<<<<<< HEAD
                    'message': 'Failed to register user'
=======
<<<<<<< HEAD
                    'message': 'Failed to register user'
=======
                    'message': 'Registration failed'
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                }
                
        except Exception as e:
            logging.error(f"Registration error: {e}")
            return {
                'success': False,
                'message': 'Registration failed due to system error'
            }
    
    @staticmethod
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
    def update_user_profile(user_id, name, email):
        try:
            db = DatabaseConnection()
            
            update_query = """
                UPDATE users 
                SET Name = %s, Email = %s
                WHERE UserID = %s
            """
            
            result = db.execute_query(update_query, (name, email, user_id))
            
            if result and result > 0:
<<<<<<< HEAD
=======
=======
    def email_exists(email):
        """
        Check if email already exists in database
        
        Args:
            email (str): Email to check
        
        Returns:
            bool: True if email exists, False otherwise
        """
        try:
            query = "SELECT COUNT(*) as count FROM users WHERE Email = %s"
            result = db.execute_query(query, (email,), fetch_one=True)
            
            return result and result['count'] > 0
            
        except Exception as e:
            logging.error(f"Email check error: {e}")
            return False
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user information by user ID
        
        Args:
            user_id (str): User ID
        
        Returns:
            dict/None: User data if found, None otherwise
        """
        try:
            query = """
                SELECT UserID, Name, Email, Role 
                FROM users 
                WHERE UserID = %s
            """
            
            user = db.execute_query(query, (user_id,), fetch_one=True)
            return user
            
        except Exception as e:
            logging.error(f"Get user error: {e}")
            return None
    
    @staticmethod
    def update_user_profile(user_id, name, email):
        """
        Update user profile information
        
        Args:
            user_id (str): User ID
            name (str): New name
            email (str): New email
        
        Returns:
            dict: Result with success status and message
        """
        try:
            # Check if new email already exists for different user
            existing_query = """
                SELECT COUNT(*) as count 
                FROM users 
                WHERE Email = %s AND UserID != %s
            """
            existing = db.execute_query(
                existing_query, 
                (email, user_id), 
                fetch_one=True
            )
            
            if existing and existing['count'] > 0:
                return {
                    'success': False,
                    'message': 'Email already in use by another user'
                }
            
            # Update user information
            update_query = """
                UPDATE users 
                SET Name = %s, Email = %s 
                WHERE UserID = %s
            """
            
            result = db.execute_query(
                update_query, 
                (name, email, user_id),
                fetch_all=False
            )
            
            if result:
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                return {
                    'success': True,
                    'message': 'Profile updated successfully'
                }
            else:
                return {
                    'success': False,
<<<<<<< HEAD
                    'message': 'Failed to update profile'
=======
<<<<<<< HEAD
                    'message': 'Failed to update profile'
=======
                    'message': 'Profile update failed'
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                }
                
        except Exception as e:
            logging.error(f"Profile update error: {e}")
            return {
                'success': False,
                'message': 'Profile update failed due to system error'
            }
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
        try:
            db = DatabaseConnection()
            
            # Verify old password
            query = "SELECT Password FROM users WHERE UserID = %s"
            user = db.execute_query(query, (user_id,), fetch_one=True)
            
            if not user or not UserModel._verify_password(old_password, user['Password']):
<<<<<<< HEAD
=======
=======
        """
        Change user password
        
        Args:
            user_id (str): User ID
            old_password (str): Current password
            new_password (str): New password
        
        Returns:
            dict: Result with success status and message
        """
        try:
            # Verify old password
            old_hashed = UserModel.hash_password(old_password)
            verify_query = """
                SELECT COUNT(*) as count 
                FROM users 
                WHERE UserID = %s AND Password = %s
            """
            
            verify_result = db.execute_query(
                verify_query, 
                (user_id, old_hashed), 
                fetch_one=True
            )
            
            if not verify_result or verify_result['count'] == 0:
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                return {
                    'success': False,
                    'message': 'Current password is incorrect'
                }
            
            # Update password
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            hashed_new_password = UserModel._hash_password(new_password)
            update_query = "UPDATE users SET Password = %s WHERE UserID = %s"
            
            result = db.execute_query(update_query, (hashed_new_password, user_id))
            
            if result and result > 0:
<<<<<<< HEAD
=======
=======
            new_hashed = UserModel.hash_password(new_password)
            update_query = """
                UPDATE users 
                SET Password = %s 
                WHERE UserID = %s
            """
            
            result = db.execute_query(
                update_query, 
                (new_hashed, user_id),
                fetch_all=False
            )
            
            if result:
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                return {
                    'success': True,
                    'message': 'Password changed successfully'
                }
            else:
                return {
                    'success': False,
<<<<<<< HEAD
                    'message': 'Failed to change password'
=======
<<<<<<< HEAD
                    'message': 'Failed to change password'
=======
                    'message': 'Password change failed'
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                }
                
        except Exception as e:
            logging.error(f"Password change error: {e}")
            return {
                'success': False,
                'message': 'Password change failed due to system error'
            }
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
    
    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def _verify_password(password, hashed_password):
        return UserModel._hash_password(password) == hashed_password
<<<<<<< HEAD
=======
=======
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
