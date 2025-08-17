from app.utils.database import Database
import uuid


class Book:
    @staticmethod
    def get_all_books():
        try:
            query = """
            SELECT book_id, title, author, subject, isbn, status 
            FROM books 
            ORDER BY title
            """
            result = Database.execute_query(query)
            return result if result else []
        except:
            return []
    
    @staticmethod
    def add_book(title, author, subject, isbn):
        try:
            book_id = str(uuid.uuid4())
            connection = Database.get_connection()
            if connection:
                cursor = connection.cursor()
                query = """
                INSERT INTO books (book_id, title, author, subject, isbn, status) 
                VALUES (%s, %s, %s, %s, %s, 'Available')
                """
                cursor.execute(query, (book_id, title, author, subject, isbn))
                connection.commit()
                cursor.close()
                connection.close()
                return True
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
        return False
    
    @staticmethod
    def get_book_by_id(book_id):
        try:
            query = "SELECT * FROM books WHERE book_id = %s"
            result = Database.execute_single_query(query, (book_id,))
            return result
        except:
            return None
    
    @staticmethod
    def update_book(book_id, title, author, subject, isbn):
        try:
            connection = Database.get_connection()
            if connection:
                cursor = connection.cursor()
                query = """
                UPDATE books 
                SET title = %s, author = %s, subject = %s, isbn = %s 
                WHERE book_id = %s
                """
                cursor.execute(query, (title, author, subject, isbn, book_id))
                connection.commit()
                result = cursor.rowcount > 0
                cursor.close()
                connection.close()
                return result
        except Exception as e:
            print(f"Error updating book: {e}")
            return False
        return False
    
    @staticmethod
    def delete_book(book_id):
        try:
            connection = Database.get_connection()
            if connection:
                cursor = connection.cursor()
                
                check_query = "SELECT status FROM books WHERE book_id = %s"
                cursor.execute(check_query, (book_id,))
                book = cursor.fetchone()
                
                if not book:
                    cursor.close()
                    connection.close()
                    return False
                
                if book[0] == 'Borrowed':
                    cursor.close()
                    connection.close()
                    return "borrowed"
                
                delete_query = "DELETE FROM books WHERE book_id = %s"
                cursor.execute(delete_query, (book_id,))
                connection.commit()
                result = cursor.rowcount > 0
                cursor.close()
                connection.close()
                return result
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False
        return False
    
    @staticmethod
    def initialize_sample_data():
        try:
            existing_books = Database.execute_query("SELECT COUNT(*) as count FROM books")
            if existing_books and existing_books[0]['count'] > 0:
                return True
            
            sample_books = [
                ('book-001', 'Python Programming', 'John Smith', 'Computer Science', '978-1234567890', 'Available'),
                ('book-002', 'Web Development', 'Jane Doe', 'Computer Science', '978-0987654321', 'Available'),
                ('book-003', 'Database Design', 'Bob Johnson', 'Computer Science', '978-1122334455', 'Available'),
                ('book-004', 'Mathematics', 'Alice Brown', 'Mathematics', '978-5566778899', 'Available'),
                ('book-005', 'Physics Fundamentals', 'Charlie Wilson', 'Physics', '978-9988776655', 'Available'),
                ('book-006', 'Chemistry Basics', 'David Lee', 'Chemistry', '978-1357924680', 'Available'),
                ('book-007', 'History of Art', 'Emma White', 'Arts', '978-2468135790', 'Available'),
                ('book-008', 'Literature Analysis', 'Frank Green', 'Literature', '978-3691470258', 'Available')
            ]
            
            for book in sample_books:
                query = """
                INSERT INTO books (book_id, title, author, subject, isbn, status) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                Database.execute_insert_query(query, book)
            
            return True
            
        except Exception as e:
            print(f"Error initializing sample data: {e}")
            return False