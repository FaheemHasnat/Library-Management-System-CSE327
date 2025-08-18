from app.utils.database import Database
import hashlib
import uuid


class User:
    @staticmethod
    def get_all_books():
        try:
            User.initialize_sample_books()
            query = "SELECT * FROM books"
            books_data = Database.execute_query(query)
            books = []
            if books_data:
                for book in books_data:
                    books.append({
                        'title': book.get('title', ''),
                        'author': book.get('author', ''),
                        'subject': book.get('subject', ''),
                        'isbn': book.get('isbn', ''),
                        'status': book.get('status', '')
                    })
            return books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
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
    
    @staticmethod
    def initialize_sample_data():
        try:
            Database.execute_insert_query("CREATE TABLE IF NOT EXISTS users (UserID VARCHAR(50) PRIMARY KEY, Name VARCHAR(255), Email VARCHAR(255) UNIQUE, Password VARCHAR(255), Role VARCHAR(50))", ())
            
            existing_admin = Database.execute_query("SELECT COUNT(*) as count FROM users WHERE Role = 'Admin'")
            if existing_admin and existing_admin[0]['count'] > 0:
                return True
            
            sample_users = [
                ('admin-001', 'System Administrator', 'admin@lms.com', 'admin123', 'Admin'),
                ('lib-001', 'System Librarian', 'librarian@lms.com', 'lib123', 'Librarian'),
                ('student-001', 'John Student', 'student@lms.com', 'student123', 'Student')
            ]
            
            for user_data in sample_users:
                user_id, name, email, password, role = user_data
                hashed_password = User.hash_password(password)
                
                query = """
                INSERT INTO users (UserID, Name, Email, Password, Role) 
                VALUES (%s, %s, %s, %s, %s)
                """
                Database.execute_insert_query(query, (user_id, name, email, hashed_password, role))
            
            return True
            
        except Exception as e:
            print(f"Error initializing sample users: {e}")
            return False

    @staticmethod
    def initialize_sample_books():
        try:
            existing_books = Database.execute_query("SELECT COUNT(*) as count FROM books")
            if existing_books and existing_books[0]['count'] > 5:
                return True
            
            sample_books = [
                ('978-0-13-110362-7', 'The Art of Computer Programming', 'Donald Knuth', 'Computer Science', 'Available'),
                ('978-0-262-03384-8', 'Introduction to Algorithms', 'Thomas Cormen', 'Computer Science', 'Available'),
                ('978-0-321-57351-3', 'Effective Java', 'Joshua Bloch', 'Programming', 'Borrowed'),
                ('978-0-13-601970-1', 'C Programming Language', 'Brian Kernighan', 'Programming', 'Available'),
                ('978-0-596-52068-7', 'JavaScript: The Good Parts', 'Douglas Crockford', 'Web Development', 'Reserved')
            ]
            
            for book_data in sample_books:
                isbn, title, author, subject, status = book_data
                existing = Database.execute_query("SELECT COUNT(*) as count FROM books WHERE isbn = %s", (isbn,))
                if existing and existing[0]['count'] == 0:
                    query = "INSERT INTO books (isbn, title, author, subject, status) VALUES (%s, %s, %s, %s, %s)"
                    Database.execute_insert_query(query, (isbn, title, author, subject, status))
            
            return True
            
        except Exception as e:
            print(f"Error initializing sample books: {e}")
            return False
