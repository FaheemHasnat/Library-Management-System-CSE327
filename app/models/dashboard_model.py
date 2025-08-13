from datetime import datetime, timedelta
from app.utils.lms_db import DatabaseConnection
import logging


class DashboardModel:
    
    @staticmethod
    def get_system_statistics():
        try:
            db = DatabaseConnection()
            stats = {}
            
            user_query = "SELECT Role, COUNT(*) as count FROM users GROUP BY Role"
            user_results = db.execute_query(user_query)
            
            stats['users'] = {
                'total': 0,
                'students': 0,
                'librarians': 0,
                'admins': 0
            }
            
            if user_results:
                for row in user_results:
                    role = row['Role'].lower()
                    count = row['count']
                    stats['users']['total'] += count
                    
                    if role == 'student':
                        stats['users']['students'] = count
                    elif role == 'librarian':
                        stats['users']['librarians'] = count
                    elif role == 'admin':
                        stats['users']['admins'] = count
            
            book_stats_query = """
                SELECT 
                    COUNT(*) as total_books,
                    SUM(CASE WHEN Status = 'Available' THEN 1 ELSE 0 END) as available_books,
                    SUM(CASE WHEN Status = 'Issued' THEN 1 ELSE 0 END) as issued_books,
                    SUM(CASE WHEN Status = 'Reserved' THEN 1 ELSE 0 END) as reserved_books
                FROM book
            """
            
            book_stats = db.execute_query(book_stats_query, fetch_one=True)
            
            stats['books'] = {
                'total': book_stats['total_books'] if book_stats else 0,
                'available': book_stats['available_books'] if book_stats else 0,
                'issued': book_stats['issued_books'] if book_stats else 0,
                'reserved': book_stats['reserved_books'] if book_stats else 0
            }
            
            transaction_stats_query = """
                SELECT 
                    COUNT(*) as total_transactions,
                    SUM(CASE WHEN ReturnDate IS NULL THEN 1 ELSE 0 END) as active_transactions,
                    SUM(CASE WHEN DueDate < CURDATE() AND ReturnDate IS NULL THEN 1 ELSE 0 END) as overdue_transactions,
                    SUM(Fine) as total_fines
                FROM transaction
            """
            
            trans_stats = db.execute_query(transaction_stats_query, fetch_one=True)
            
            stats['transactions'] = {
                'total': trans_stats['total_transactions'] if trans_stats else 0,
                'active': trans_stats['active_transactions'] if trans_stats else 0,
                'overdue': trans_stats['overdue_transactions'] if trans_stats else 0,
                'total_fines': float(trans_stats['total_fines']) if trans_stats and trans_stats['total_fines'] else 0.0
            }
            
            reservation_stats_query = """
                SELECT COUNT(*) as total_reservations
                FROM reservation
                WHERE Status = 'Active'
            """
            
            reservation_stats = db.execute_query(reservation_stats_query, fetch_one=True)
            stats['reservations'] = reservation_stats['total_reservations'] if reservation_stats else 0
            
            return stats
            
        except Exception as e:
            logging.error(f"Error getting system statistics: {e}")
            return None
    
    @staticmethod
    def get_librarian_statistics():
        try:
            db = DatabaseConnection()
            stats = {}
            
            book_stats_query = """
                SELECT 
                    COUNT(*) as total_books,
                    SUM(CASE WHEN Status = 'Available' THEN 1 ELSE 0 END) as available_books,
                    SUM(CASE WHEN Status = 'Issued' THEN 1 ELSE 0 END) as issued_books,
                    SUM(CASE WHEN Status = 'Reserved' THEN 1 ELSE 0 END) as reserved_books
                FROM book
            """
            
            book_stats = db.execute_query(book_stats_query, fetch_one=True)
            
            stats['books'] = {
                'total': book_stats['total_books'] if book_stats else 0,
                'available': book_stats['available_books'] if book_stats else 0,
                'issued': book_stats['issued_books'] if book_stats else 0,
                'reserved': book_stats['reserved_books'] if book_stats else 0
            }
            
            transaction_stats_query = """
                SELECT 
                    COUNT(*) as total_transactions,
                    SUM(CASE WHEN ReturnDate IS NULL THEN 1 ELSE 0 END) as active_transactions,
                    SUM(CASE WHEN DueDate < CURDATE() AND ReturnDate IS NULL THEN 1 ELSE 0 END) as overdue_transactions
                FROM transaction
            """
            
            trans_stats = db.execute_query(transaction_stats_query, fetch_one=True)
            
            stats['transactions'] = {
                'total': trans_stats['total_transactions'] if trans_stats else 0,
                'active': trans_stats['active_transactions'] if trans_stats else 0,
                'overdue': trans_stats['overdue_transactions'] if trans_stats else 0
            }
            
            reservation_stats_query = """
                SELECT COUNT(*) as active_reservations
                FROM reservation
                WHERE Status = 'Active'
            """
            
            reservation_stats = db.execute_query(reservation_stats_query, fetch_one=True)
            stats['reservations'] = reservation_stats['active_reservations'] if reservation_stats else 0
            
            return stats
            
        except Exception as e:
            logging.error(f"Error getting librarian statistics: {e}")
            return None
    
    @staticmethod
    def get_student_statistics(user_id):
        try:
            db = DatabaseConnection()
            stats = {}
            
            issued_books_query = """
                SELECT COUNT(*) as issued_count
                FROM transaction
                WHERE UserID = %s AND ReturnDate IS NULL
            """
            
            issued_result = db.execute_query(issued_books_query, (user_id,), fetch_one=True)
            stats['issued_books'] = issued_result['issued_count'] if issued_result else 0
            
            overdue_query = """
                SELECT COUNT(*) as overdue_count 
                FROM transaction 
                WHERE UserID = %s AND DueDate < CURDATE() AND ReturnDate IS NULL
            """
            
            overdue_result = db.execute_query(overdue_query, (user_id,), fetch_one=True)
            stats['overdue_books'] = overdue_result['overdue_count'] if overdue_result else 0
            
            due_today_query = """
                SELECT COUNT(*) as due_today_count
                FROM transaction
                WHERE UserID = %s AND DueDate = CURDATE() AND ReturnDate IS NULL
            """
            
            due_today_result = db.execute_query(due_today_query, (user_id,), fetch_one=True)
            stats['due_today'] = due_today_result['due_today_count'] if due_today_result else 0
            
            reservations_query = """
                SELECT COUNT(*) as active_reservations
                FROM reservation
                WHERE UserID = %s AND Status = 'Active'
            """
            
            reservations_result = db.execute_query(reservations_query, (user_id,), fetch_one=True)
            stats['active_reservations'] = reservations_result['active_reservations'] if reservations_result else 0
            
            fines_query = """
                SELECT SUM(Fine) as total_fines
                FROM transaction
                WHERE UserID = %s AND Fine > 0
            """
            
            fines_result = db.execute_query(fines_query, (user_id,), fetch_one=True)
            stats['total_fines'] = float(fines_result['total_fines']) if fines_result and fines_result['total_fines'] else 0.0
            
            return stats
            
        except Exception as e:
            logging.error(f"Error getting student statistics: {e}")
            return None
    
    @staticmethod
    def get_recent_notifications(user_id, user_role, limit=5):
        try:
            db = DatabaseConnection()
            
            if user_role in ['Admin', 'Librarian']:
                query = """
                    SELECT NotificationID, Message, CreatedAt, Type, IsRead
                    FROM notification
                    ORDER BY CreatedAt DESC
                    LIMIT %s
                """
                params = (limit,)
            else:
                query = """
                    SELECT NotificationID, Message, CreatedAt, Type, IsRead
                    FROM notification
                    WHERE UserID = %s
                    ORDER BY CreatedAt DESC
                    LIMIT %s
                """
                params = (user_id, limit)
            
            notifications = db.execute_query(query, params)
            return notifications or []
            
        except Exception as e:
            logging.error(f"Error getting recent notifications: {e}")
            return []
    
    @staticmethod
    def get_overdue_books_details(user_role, user_id=None):
        try:
            db = DatabaseConnection()
            
            if user_role == 'Student':
                query = """
                    SELECT b.Title, b.Author, t.DueDate, t.Fine,
                           DATEDIFF(CURDATE(), t.DueDate) as days_overdue
                    FROM transaction t
                    JOIN book b ON t.BookID = b.BookID
                    WHERE t.UserID = %s AND t.DueDate < CURDATE() AND t.ReturnDate IS NULL
                    ORDER BY t.DueDate ASC
                """
                params = (user_id,)
            else:
                query = """
                    SELECT u.Name as student_name, b.Title, b.Author, t.DueDate, t.Fine,
                           DATEDIFF(CURDATE(), t.DueDate) as days_overdue
                    FROM transaction t
                    JOIN book b ON t.BookID = b.BookID
                    JOIN users u ON t.UserID = u.UserID
                    WHERE t.DueDate < CURDATE() AND t.ReturnDate IS NULL
                    ORDER BY t.DueDate ASC
                    LIMIT 10
                """
                params = ()
            
            overdue_books = db.execute_query(query, params)
            return overdue_books or []
            
        except Exception as e:
            logging.error(f"Error getting overdue books details: {e}")
            return []
    
    @staticmethod
    def get_recent_transactions(user_role, user_id=None, limit=5):
        try:
            db = DatabaseConnection()
            
            if user_role == 'Student':
                query = """
                    SELECT b.Title, b.Author, t.IssueDate, t.DueDate, t.ReturnDate
                    FROM transaction t
                    JOIN book b ON t.BookID = b.BookID
                    WHERE t.UserID = %s
                    ORDER BY t.IssueDate DESC
                    LIMIT %s
                """
                params = (user_id, limit)
            else:
                query = """
                    SELECT u.Name as student_name, b.Title, b.Author, 
                           t.IssueDate, t.DueDate, t.ReturnDate
                    FROM transaction t
                    JOIN book b ON t.BookID = b.BookID
                    JOIN users u ON t.UserID = u.UserID
                    ORDER BY t.IssueDate DESC
                    LIMIT %s
                """
                params = (limit,)
            
            transactions = db.execute_query(query, params)
            return transactions or []
            
        except Exception as e:
            logging.error(f"Error getting recent transactions: {e}")
            return []
    
    @staticmethod
    def mark_notification_read(notification_id):
        try:
            db = DatabaseConnection()
            
            query = """
                UPDATE notification
                SET IsRead = 1
                WHERE NotificationID = %s
            """
            
            result = db.execute_query(query, (notification_id,))
            return result is not None and result > 0
            
        except Exception as e:
            logging.error(f"Error marking notification as read: {e}")
            return False
