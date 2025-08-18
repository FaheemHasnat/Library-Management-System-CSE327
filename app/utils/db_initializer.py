from app.models.book import Book
from app.models.user import User


class DatabaseInitializer:
    @staticmethod
    def initialize_all():
        try:
            print("Initializing database...")
            
            DatabaseInitializer.create_tables()
            
            Book.initialize_sample_data()
            print("✓ Sample books initialized")
            
            User.initialize_sample_data()
            print("✓ Sample users initialized")
            
            print("✓ Database initialization complete")
            return True
            
        except Exception as e:
            print(f"✗ Database initialization failed: {e}")
            return False
    
    @staticmethod
    def create_tables():
        from app.utils.database import Database
        
        try:
            users_table = """
            CREATE TABLE IF NOT EXISTS users (
                UserID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                Email VARCHAR(255) UNIQUE NOT NULL,
                Password VARCHAR(255) NOT NULL,
                Role ENUM('Admin', 'Librarian', 'Student') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            books_table = """
            CREATE TABLE IF NOT EXISTS books (
                book_id VARCHAR(50) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                subject VARCHAR(100) NOT NULL,
                isbn VARCHAR(20) NOT NULL,
                status ENUM('Available', 'Borrowed', 'Reserved') DEFAULT 'Available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            reservations_table = """
            CREATE TABLE IF NOT EXISTS book_reservations (
                reservation_id VARCHAR(50) PRIMARY KEY,
                book_id VARCHAR(50),
                user_id INT,
                reservation_date DATE,
                status ENUM('Active', 'Fulfilled', 'Cancelled') DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(UserID) ON DELETE CASCADE
            )
            """
            
            Database.execute_insert_query(users_table)
            Database.execute_insert_query(books_table)
            Database.execute_insert_query(reservations_table)
            
            print("✓ Database tables created")
            return True
            
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            return False
