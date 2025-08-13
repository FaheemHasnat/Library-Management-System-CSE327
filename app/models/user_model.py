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
            
        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return None
    
    @staticmethod
    def register_user(name, email, password, role='Student'):
        try:
            db = DatabaseConnection()
            
            # Check if email already exists
            check_query = "SELECT UserID FROM users WHERE Email = %s"
            existing_user = db.execute_query(check_query, (email,), fetch_one=True)
            
            if existing_user:
                return {
                    'success': False,
                    'message': 'Email already registered'
                }
            
            # Create new user
            user_id = str(uuid.uuid4())
            hashed_password = UserModel._hash_password(password)
            
            insert_query = """
                INSERT INTO users (UserID, Name, Email, Password, Role)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            result = db.execute_query(insert_query, (user_id, name, email, hashed_password, role))
            
            if result:
                return {
                    'success': True,
                    'message': 'User registered successfully',
                    'user_id': user_id
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to register user'
                }
                
        except Exception as e:
            logging.error(f"Registration error: {e}")
            return {
                'success': False,
                'message': 'Registration failed due to system error'
            }
    
    @staticmethod
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
                return {
                    'success': True,
                    'message': 'Profile updated successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to update profile'
                }
                
        except Exception as e:
            logging.error(f"Profile update error: {e}")
            return {
                'success': False,
                'message': 'Profile update failed due to system error'
            }
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        try:
            db = DatabaseConnection()
            
            # Verify old password
            query = "SELECT Password FROM users WHERE UserID = %s"
            user = db.execute_query(query, (user_id,), fetch_one=True)
            
            if not user or not UserModel._verify_password(old_password, user['Password']):
                return {
                    'success': False,
                    'message': 'Current password is incorrect'
                }
            
            # Update password
            hashed_new_password = UserModel._hash_password(new_password)
            update_query = "UPDATE users SET Password = %s WHERE UserID = %s"
            
            result = db.execute_query(update_query, (hashed_new_password, user_id))
            
            if result and result > 0:
                return {
                    'success': True,
                    'message': 'Password changed successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to change password'
                }
                
        except Exception as e:
            logging.error(f"Password change error: {e}")
            return {
                'success': False,
                'message': 'Password change failed due to system error'
            }
    
    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def _verify_password(password, hashed_password):
        return UserModel._hash_password(password) == hashed_password
