from app.utils.database import Database
import mysql.connector
from config import Config


def create_database():
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Database {Config.DB_NAME} created successfully")
    except Exception as e:
        print(f"Error creating database: {e}")


def create_tables():
    create_books_table = """
    CREATE TABLE IF NOT EXISTS books (
        book_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        isbn VARCHAR(20) UNIQUE,
        category VARCHAR(100),
        status ENUM('Available', 'Issued', 'Reserved', 'Maintenance') DEFAULT 'Available',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """
    
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        role ENUM('Admin', 'Librarian', 'Student') NOT NULL,
        status ENUM('Active', 'Inactive') DEFAULT 'Active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    create_book_issues_table = """
    CREATE TABLE IF NOT EXISTS book_issues (
        issue_id INT AUTO_INCREMENT PRIMARY KEY,
        book_id INT NOT NULL,
        user_id INT NOT NULL,
        issue_date DATE NOT NULL,
        due_date DATE NOT NULL,
        return_date DATE NULL,
        status ENUM('Issued', 'Returned', 'Overdue') DEFAULT 'Issued',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (book_id) REFERENCES books(book_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """
    
    create_book_reservations_table = """
    CREATE TABLE IF NOT EXISTS book_reservations (
        reservation_id INT AUTO_INCREMENT PRIMARY KEY,
        book_id INT NOT NULL,
        user_id INT NOT NULL,
        reservation_date DATE NOT NULL,
        expiry_date DATE DEFAULT (DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
        status ENUM('Active', 'Fulfilled', 'Cancelled', 'Expired') DEFAULT 'Active',
        notes TEXT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        UNIQUE KEY unique_active_reservation (book_id, user_id, status)
    )
    """
    
    tables = [create_books_table, create_users_table, create_book_issues_table, create_book_reservations_table]
    
    connection = Database.get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            for table_query in tables:
                cursor.execute(table_query)
            connection.commit()
            print("All tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
            connection.close()


def insert_sample_data():
    sample_books = """
    INSERT IGNORE INTO books (title, author, isbn, category, status) VALUES
    ('Python Programming', 'John Doe', '978-1234567890', 'Programming', 'Available'),
    ('Web Development', 'Jane Smith', '978-1234567891', 'Programming', 'Issued'),
    ('Database Design', 'Bob Johnson', '978-1234567892', 'Database', 'Available'),
    ('Data Structures', 'Alice Brown', '978-1234567893', 'Programming', 'Reserved'),
    ('Machine Learning', 'Charlie Wilson', '978-1234567894', 'AI', 'Available'),
    ('Flask Framework', 'David Lee', '978-1234567895', 'Web', 'Issued'),
    ('MySQL Guide', 'Eva Green', '978-1234567896', 'Database', 'Available'),
    ('JavaScript Basics', 'Frank White', '978-1234567897', 'Programming', 'Available'),
    ('CSS Styling', 'Grace Taylor', '978-1234567898', 'Web', 'Issued'),
    ('HTML Fundamentals', 'Henry Adams', '978-1234567899', 'Web', 'Available'),
    ('Advanced Python', 'Mike Johnson', '978-1234567900', 'Programming', 'Available'),
    ('React.js Guide', 'Sarah Lee', '978-1234567901', 'Web', 'Available'),
    ('Node.js Basics', 'Tom Brown', '978-1234567902', 'Backend', 'Available'),
    ('SQL Mastery', 'Lisa White', '978-1234567903', 'Database', 'Available'),
    ('Algorithm Design', 'Mark Davis', '978-1234567904', 'Programming', 'Available')
    """
    
    sample_users = """
    INSERT IGNORE INTO users (username, email, password_hash, full_name, role) VALUES
    ('admin', 'admin@lms.com', 'hashed_password', 'System Administrator', 'Admin'),
    ('librarian1', 'librarian@lms.com', 'hashed_password', 'Library Manager', 'Librarian'),
    ('student1', 'student1@lms.com', 'hashed_password', 'John Student', 'Student'),
    ('student2', 'student2@lms.com', 'hashed_password', 'Jane Student', 'Student'),
    ('student3', 'student3@lms.com', 'hashed_password', 'Mike Wilson', 'Student'),
    ('student4', 'student4@lms.com', 'hashed_password', 'Sarah Davis', 'Student'),
    ('student5', 'student5@lms.com', 'hashed_password', 'Tom Anderson', 'Student')
    """
    
    sample_issues = """
    INSERT IGNORE INTO book_issues (book_id, user_id, issue_date, due_date, status) VALUES
    (2, 3, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), 'Issued'),
    (6, 4, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY), 'Issued'),
    (9, 3, DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_SUB(CURDATE(), INTERVAL 6 DAY), 'Issued')
    """
    
    sample_reservations = """
    INSERT IGNORE INTO book_reservations (book_id, user_id, reservation_date, status) VALUES
    (4, 4, CURDATE(), 'Active'),
    (1, 3, CURDATE(), 'Active')
    """
    
    queries = [sample_books, sample_users, sample_issues, sample_reservations]
    
    connection = Database.get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            for query in queries:
                cursor.execute(query)
            connection.commit()
            print("Sample data inserted successfully")
        except Exception as e:
            print(f"Error inserting sample data: {e}")
        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    create_database()
    create_tables()
    insert_sample_data()
