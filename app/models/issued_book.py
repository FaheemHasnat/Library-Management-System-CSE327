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
    def get_transaction_history():
        query = """
        SELECT t.TransactionID, t.UserID, t.BookID, t.IssueDate, t.DueDate, 
               t.ReturnDate, t.Fine,
               COALESCE(b.title, 'Unknown Book') as book_title,
               COALESCE(b.author, 'Unknown Author') as book_author,
               COALESCE(u.Name, 'Unknown Student') as student_name,
               COALESCE(u.Email, 'Unknown Email') as student_email
        FROM transaction t
        LEFT JOIN books b ON t.BookID = b.book_id
        LEFT JOIN users u ON t.UserID = u.UserID
        ORDER BY t.ReturnDate DESC
        """
        result = Database.execute_query(query)
        return result if result else []
    
    @staticmethod
    def get_users_with_fines():
        query = """
        SELECT t.TransactionID, t.UserID, t.BookID, t.IssueDate, t.DueDate, 
               t.ReturnDate, t.Fine,
               COALESCE(u.Name, 'Unknown Student') as student_name,
               COALESCE(u.Email, 'Unknown Email') as student_email,
               COALESCE(b.Title, 'Unknown Book') as book_title,
               COALESCE(b.Author, 'Unknown Author') as book_author
        FROM transaction t
        LEFT JOIN users u ON t.UserID = u.UserID
        LEFT JOIN book b ON t.BookID = b.BookID
        WHERE t.Fine > 0
        ORDER BY t.Fine DESC, t.ReturnDate DESC
        """
        result = Database.execute_query(query)
        return result if result else []
    
    @staticmethod
    def get_fines_summary():
        query = """
        SELECT 
            SUM(Fine) as total_outstanding,
            COUNT(*) as total_fines,
            SUM(CASE WHEN DATE(ReturnDate) = CURDATE() THEN Fine ELSE 0 END) as collected_today
        FROM transaction 
        WHERE Fine > 0
        """
        result = Database.execute_single_query(query)
        return {
            'total_outstanding': result.get('total_outstanding', 0) or 0,
            'total_fines': result.get('total_fines', 0) or 0,
            'collected_today': result.get('collected_today', 0) or 0
        } if result else {'total_outstanding': 0, 'total_fines': 0, 'collected_today': 0}
    
    @staticmethod
    def get_student_fines(user_id):
        query = """
        SELECT SUM(Fine) as total_fines
        FROM transaction 
        WHERE UserID = %s AND Fine > 0
        """
        result = Database.execute_single_query(query, (user_id,))
        return result.get('total_fines', 0) if result and result.get('total_fines') else 0
    
    @staticmethod
    def get_student_fine_history(user_id):
        query = """
        SELECT t.TransactionID, t.UserID, t.BookID, t.IssueDate, t.DueDate, 
               t.ReturnDate, t.Fine,
               COALESCE(b.title, 'Unknown Book') as book_title,
               COALESCE(b.author, 'Unknown Author') as book_author
        FROM transaction t
        LEFT JOIN books b ON t.BookID = b.book_id
        WHERE t.UserID = %s AND t.Fine > 0
        ORDER BY t.ReturnDate DESC
        """
        result = Database.execute_query(query, (user_id,))
        return result if result else []
    
    @staticmethod
    def return_book(user_id, book_id, return_date_str):
        connection = Database.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            check_issued_query = """
            SELECT issueID, issue_date, due_date FROM issued_books 
            WHERE UserID = %s AND book_id = %s
            """
            cursor.execute(check_issued_query, (user_id, book_id))
            issued_record = cursor.fetchone()
            
            if not issued_record:
                return False
            
            issue_id, issue_date, due_date = issued_record
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
            
            fine_amount = 0.00
            if return_date > due_date:
                days_late = (return_date - due_date).days
                fine_amount = days_late * 10.00
            
            get_valid_book_uuid_query = """
            SELECT BookID FROM book LIMIT 1
            """
            cursor.execute(get_valid_book_uuid_query)
            book_uuid_result = cursor.fetchone()
            book_uuid = book_uuid_result[0] if book_uuid_result else str(book_id)
            
            insert_transaction_query = """
            INSERT INTO transaction (UserID, BookID, IssueDate, DueDate, ReturnDate, Fine)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_transaction_query, (user_id, book_uuid, issue_date, due_date, return_date, fine_amount))
            
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
            return {'success': True, 'fine': fine_amount}
        except Exception as e:
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()