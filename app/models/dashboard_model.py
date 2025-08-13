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
<<<<<<< HEAD
            
=======
<<<<<<< HEAD
            
=======
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
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
<<<<<<< HEAD
            
=======
<<<<<<< HEAD
            
=======
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                WHERE Status = 'Active'
            """
            
            reservation_stats = db.execute_query(reservation_stats_query, fetch_one=True)
            stats['reservations'] = reservation_stats['total_reservations'] if reservation_stats else 0
<<<<<<< HEAD
=======
=======
            """
            res_stats = db.execute_query(reservation_stats_query, fetch_one=True)
            
            stats['reservations'] = {
                'total': res_stats['total_reservations'] if res_stats else 0,
                'active': 0,
                'cancelled': 0
            }
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            
            return stats
            
        except Exception as e:
<<<<<<< HEAD
            logging.error(f"Error getting system statistics: {e}")
=======
<<<<<<< HEAD
            logging.error(f"Error getting system statistics: {e}")
=======
            logging.error(f"Error fetching system statistics: {e}")
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            return None
    
    @staticmethod
    def get_librarian_statistics():
        try:
            db = DatabaseConnection()
            stats = {}
            
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
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
<<<<<<< HEAD
=======
=======
            issued_query = """
                SELECT COUNT(*) as issued_count 
                FROM transaction 
                WHERE ReturnDate IS NULL
            """
            issued_result = db.execute_query(issued_query, fetch_one=True)
            stats['issued_books'] = issued_result['issued_count'] if issued_result else 0
            
            overdue_query = """
                SELECT COUNT(*) as overdue_count 
                FROM transaction 
                WHERE DueDate < CURDATE() AND ReturnDate IS NULL
            """
            overdue_result = db.execute_query(overdue_query, fetch_one=True)
            stats['overdue_books'] = overdue_result['overdue_count'] if overdue_result else 0
            
            due_today_query = """
                SELECT COUNT(*) as due_today_count 
                FROM transaction 
                WHERE DueDate = CURDATE() AND ReturnDate IS NULL
            """
            due_today_result = db.execute_query(due_today_query, fetch_one=True)
            stats['due_today'] = due_today_result['due_today_count'] if due_today_result else 0
            
            pending_reservations_query = """
                SELECT COUNT(*) as pending_count 
                FROM reservation
            """
            pending_result = db.execute_query(pending_reservations_query, fetch_one=True)
            stats['pending_reservations'] = pending_result['pending_count'] if pending_result else 0
            
            available_query = """
                SELECT COUNT(*) as available_count 
                FROM book 
                WHERE Status = 'Available'
            """
            available_result = db.execute_query(available_query, fetch_one=True)
            stats['available_books'] = available_result['available_count'] if available_result else 0
            
            fines_query = """
                SELECT SUM(Fine) as total_fines 
                FROM transaction 
                WHERE Fine > 0
            """
            fines_result = db.execute_query(fines_query, fetch_one=True)
            stats['total_fines'] = float(fines_result['total_fines']) if fines_result and fines_result['total_fines'] else 0.0
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            
            return stats
            
        except Exception as e:
<<<<<<< HEAD
            logging.error(f"Error getting librarian statistics: {e}")
=======
<<<<<<< HEAD
            logging.error(f"Error getting librarian statistics: {e}")
=======
            logging.error(f"Error fetching librarian statistics: {e}")
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            return None
    
    @staticmethod
    def get_student_statistics(user_id):
        try:
            db = DatabaseConnection()
            stats = {}
            
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            issued_books_query = """
                SELECT COUNT(*) as issued_count
                FROM transaction
                WHERE UserID = %s AND ReturnDate IS NULL
            """
            
            issued_result = db.execute_query(issued_books_query, (user_id,), fetch_one=True)
            stats['issued_books'] = issued_result['issued_count'] if issued_result else 0
<<<<<<< HEAD
=======
=======
            borrowed_query = """
                SELECT COUNT(*) as borrowed_count 
                FROM transaction 
                WHERE UserID = %s AND ReturnDate IS NULL
            """
            borrowed_result = db.execute_query(borrowed_query, (user_id,), fetch_one=True)
            stats['borrowed_books'] = borrowed_result['borrowed_count'] if borrowed_result else 0
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            
            overdue_query = """
                SELECT COUNT(*) as overdue_count 
                FROM transaction 
                WHERE UserID = %s AND DueDate < CURDATE() AND ReturnDate IS NULL
            """
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            
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
<<<<<<< HEAD
=======
=======
            overdue_result = db.execute_query(overdue_query, (user_id,), fetch_one=True)
            stats['overdue_books'] = overdue_result['overdue_count'] if overdue_result else 0
            
            due_soon_query = """
                SELECT COUNT(*) as due_soon_count 
                FROM transaction 
                WHERE UserID = %s 
                AND DueDate BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 3 DAY)
                AND ReturnDate IS NULL
            """
            due_soon_result = db.execute_query(due_soon_query, (user_id,), fetch_one=True)
            stats['due_soon'] = due_soon_result['due_soon_count'] if due_soon_result else 0
            
            reservations_query = """
                SELECT COUNT(*) as reservations_count 
                FROM reservation 
                WHERE UserID = %s
            """
            reservations_result = db.execute_query(reservations_query, (user_id,), fetch_one=True)
            stats['active_reservations'] = reservations_result['reservations_count'] if reservations_result else 0
            
            fines_query = """
                SELECT SUM(Fine) as total_fines 
                FROM transaction 
                WHERE UserID = %s AND Fine > 0
            """
            fines_result = db.execute_query(fines_query, (user_id,), fetch_one=True)
            stats['total_fines'] = float(fines_result['total_fines']) if fines_result and fines_result['total_fines'] else 0.0
            
            books_read_query = """
                SELECT COUNT(*) as books_read 
                FROM transaction 
                WHERE UserID = %s AND ReturnDate IS NOT NULL
            """
            books_read_result = db.execute_query(books_read_query, (user_id,), fetch_one=True)
            stats['books_read'] = books_read_result['books_read'] if books_read_result else 0
            
            return stats
            
        except Exception as e:
            logging.error(f"Error fetching student statistics: {e}")
            return None
    
    @staticmethod
    def get_recent_notifications(user_id, role, limit=5):
        try:
            db = DatabaseConnection()
            
            if role == 'Admin':
                query = """
                    SELECT n.Message, n.CreatedAt, n.IsRead,
                           u.Name as UserName
                    FROM notification n
                    LEFT JOIN users u ON n.UserID = u.UserID
                    ORDER BY n.CreatedAt DESC
                    LIMIT %s
                """
                notifications = db.execute_query(query, (limit,))
            else:
                query = """
                    SELECT Message, CreatedAt, IsRead
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                    FROM notification
                    WHERE UserID = %s
                    ORDER BY CreatedAt DESC
                    LIMIT %s
                """
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
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
<<<<<<< HEAD
=======
=======
                notifications = db.execute_query(query, (user_id, limit))
            
            return notifications if notifications else []
            
        except Exception as e:
            logging.error(f"Error fetching notifications: {e}")
            return []
    
    @staticmethod
    def get_overdue_books_details(role, user_id=None):
        try:
            db = DatabaseConnection()
            
            if role == 'Student':
                query = """
                    SELECT t.TransactionID, b.Title, b.Author, t.DueDate, t.Fine,
                           DATEDIFF(CURDATE(), t.DueDate) as DaysOverdue
                    FROM transaction t
                    INNER JOIN book b ON t.BookID = b.BookID
                    WHERE t.UserID = %s AND t.DueDate < CURDATE() AND t.ReturnDate IS NULL
                    ORDER BY t.DueDate ASC
                """
                overdue_books = db.execute_query(query, (user_id,))
            else:
                query = """
                    SELECT t.TransactionID, b.Title, b.Author, t.DueDate, t.Fine,
                           u.Name as BorrowerName, u.Email as BorrowerEmail,
                           DATEDIFF(CURDATE(), t.DueDate) as DaysOverdue
                    FROM transaction t
                    INNER JOIN book b ON t.BookID = b.BookID
                    INNER JOIN users u ON t.UserID = u.UserID
                    WHERE t.DueDate < CURDATE() AND t.ReturnDate IS NULL
                    ORDER BY t.DueDate ASC
                """
                overdue_books = db.execute_query(query)
            
            return overdue_books if overdue_books else []
            
        except Exception as e:
            logging.error(f"Error fetching overdue books: {e}")
            return []
    
    @staticmethod
    def get_recent_transactions(role, user_id=None, limit=10):
        try:
            db = DatabaseConnection()
            
            if role == 'Student':
                query = """
                    SELECT t.TransactionID, b.Title, b.Author, t.IssueDate, 
                           t.DueDate, t.ReturnDate, t.Fine
                    FROM transaction t
                    INNER JOIN book b ON t.BookID = b.BookID
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
                    WHERE t.UserID = %s
                    ORDER BY t.IssueDate DESC
                    LIMIT %s
                """
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
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
<<<<<<< HEAD
=======
=======
                transactions = db.execute_query(query, (user_id, limit))
            else:
                query = """
                    SELECT t.TransactionID, b.Title, b.Author, t.IssueDate, 
                           t.DueDate, t.ReturnDate, t.Fine, u.Name as BorrowerName
                    FROM transaction t
                    INNER JOIN book b ON t.BookID = b.BookID
                    INNER JOIN users u ON t.UserID = u.UserID
                    ORDER BY t.IssueDate DESC
                    LIMIT %s
                """
                transactions = db.execute_query(query, (limit,))
            
            return transactions if transactions else []
            
        except Exception as e:
            logging.error(f"Error fetching recent transactions: {e}")
            return []
    
    @staticmethod
    def create_notification(user_id, message):
        try:
            db = DatabaseConnection()
            
            query = """
                INSERT INTO notification (UserID, Message, CreatedAt, IsRead)
                VALUES (%s, %s, %s, 0)
            """
            
            result = db.execute_query(
                query, 
                (user_id, message, datetime.now()),
                fetch_all=False
            )
            
            return result is not None and result > 0
            
        except Exception as e:
            logging.error(f"Error creating notification: {e}")
            return False
    
    @staticmethod
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
    def mark_notification_read(notification_id):
        try:
            db = DatabaseConnection()
            
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            query = """
                UPDATE notification
                SET IsRead = 1
                WHERE NotificationID = %s
            """
            
            result = db.execute_query(query, (notification_id,))
<<<<<<< HEAD
=======
=======
            query = "UPDATE notification SET IsRead = 1 WHERE NotificationID = %s"
            
            result = db.execute_query(query, (notification_id,), fetch_all=False)
            
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
>>>>>>> b33be7ddca7312678507e52c0ced05f27ee08231
            return result is not None and result > 0
            
        except Exception as e:
            logging.error(f"Error marking notification as read: {e}")
            return False
