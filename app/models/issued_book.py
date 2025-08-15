from app.utils.database import Database
from datetime import datetime, timedelta


class IssuedBook:
    @staticmethod
    def issue_book(user_id, book_id):
        connection = Database.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            check_student_books_query = """
            SELECT COUNT(*) FROM issued_books WHERE UserID = %s
            """
            cursor.execute(check_student_books_query, (user_id,))
            borrowed_count = cursor.fetchone()[0]
            
            if borrowed_count >= 3:
                return "limit_exceeded"
            
            check_book_query = """
            SELECT status FROM books WHERE book_id = %s
            """
            cursor.execute(check_book_query, (book_id,))
            book_status = cursor.fetchone()
            
            if not book_status or book_status[0] != 'Available':
                return False
            
            issue_date = datetime.now().date()
            due_date = issue_date + timedelta(days=7)
            
            insert_query = """
            INSERT INTO issued_books (UserID, book_id, issue_date, due_date)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, book_id, issue_date, due_date))
            
            update_query = """
            UPDATE books SET status = 'Borrowed' WHERE book_id = %s
            """
            cursor.execute(update_query, (book_id,))
            
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    @staticmethod
    def get_all_issued_books():
        query = """
        SELECT ib.issue_date, ib.due_date, ib.book_id, ib.UserID,
               COALESCE(b.title, 'Unknown Book') as title,
               COALESCE(b.author, 'Unknown Author') as author,
               COALESCE(b.isbn, 'N/A') as isbn,
               COALESCE(u.Name, 'Unknown Student') as student_name,
               COALESCE(u.Email, 'Unknown Email') as student_email
        FROM issued_books ib
        LEFT JOIN books b ON ib.book_id = b.book_id
        LEFT JOIN users u ON ib.UserID = u.UserID
        ORDER BY ib.issue_date DESC
        """
        result = Database.execute_query(query)
        return result if result else []
    
    @staticmethod
    def get_available_books():
        query = """
        SELECT book_id, title, author, isbn
        FROM books
        WHERE status = 'Available'
        ORDER BY title
        """
        result = Database.execute_query(query)
        return result if result else []
    
    @staticmethod
    def get_students():
        query = """
        SELECT UserID, Name as student_name
        FROM users
        WHERE Role = 'Student'
        ORDER BY Name
        """
        result = Database.execute_query(query)
        return result if result else []
    
    @staticmethod
    def get_student_borrowed_count(user_id):
        query = """
        SELECT COUNT(*) as count FROM issued_books WHERE UserID = %s
        """
        result = Database.execute_single_query(query, (user_id,))
        return result['count'] if result else 0
    
    @staticmethod
    def return_book(user_id, book_id):
        connection = Database.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            check_issued_query = """
            SELECT issueID FROM issued_books 
            WHERE UserID = %s AND book_id = %s
            """
            cursor.execute(check_issued_query, (user_id, book_id))
            issued_record = cursor.fetchone()
            
            if not issued_record:
                return False
            
            delete_issued_query = """
            DELETE FROM issued_books 
            WHERE UserID = %s AND book_id = %s
            """
            cursor.execute(delete_issued_query, (user_id, book_id))
            
            update_book_query = """
            UPDATE books SET status = 'Available' WHERE book_id = %s
            """
            cursor.execute(update_book_query, (book_id,))
            
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()