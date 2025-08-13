from app.utils.database import Database
import hashlib
import uuid

class User:
    def __init__(self, user_id=None, name=None, email=None, password=None, role=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def authenticate(email, password):
        hashed_password = User.hash_password(password)
        query = "SELECT * FROM users WHERE Email = %s AND Password = %s"
        user_data = Database.execute_single_query(query, (email, hashed_password))
        
        if user_data:
            return User(
                user_id=user_data['UserID'],
                name=user_data['Name'],
                email=user_data['Email'],
                role=user_data['Role']
            )
        return None
    
    @staticmethod
    def get_by_email(email):
        query = "SELECT * FROM users WHERE Email = %s"
        user_data = Database.execute_single_query(query, (email,))
        
        if user_data:
            return User(
                user_id=user_data['UserID'],
                name=user_data['Name'],
                email=user_data['Email'],
                role=user_data['Role']
            )
        return None
    
    @staticmethod
    def get_by_id(user_id):
        query = "SELECT * FROM users WHERE UserID = %s"
        user_data = Database.execute_single_query(query, (user_id,))
        
        if user_data:
            return User(
                user_id=user_data['UserID'],
                name=user_data['Name'],
                email=user_data['Email'],
                role=user_data['Role']
            )
        return None
    
    @staticmethod
    def create_user(name, email, password, role):
        if User.get_by_email(email):
            return None
        
        user_id = str(uuid.uuid4())
        hashed_password = User.hash_password(password)
        
        connection = Database.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO users (UserID, Name, Email, Password, Role) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (user_id, name, email, hashed_password, role))
                connection.commit()
                
                return User(user_id=user_id, name=name, email=email, role=role)
            except Exception as e:
                print(f"Error creating user: {e}")
                return None
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return None
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }
