from datetime import datetime, timedelta
from app.utils.lms_db import DatabaseConnection
import logging
import uuid


class ReservationModel:
    
    @staticmethod
    def reserve_book(user_id, book_id):
        try:
            db = DatabaseConnection()
            
            # Check if user already has this book issued or reserved
            check_query = """
                SELECT COUNT(*) as count FROM reservation 
                WHERE UserID = %s AND BookID = %s AND Status = 'Active'
            """
            
            existing = db.execute_query(check_query, (user_id, book_id), fetch_one=True)
            if existing and existing['count'] > 0:
                return {
                    'success': False,
                    'message': 'You already have this book reserved'
                }
            
            # Create reservation
            reservation_id = str(uuid.uuid4())
            insert_query = """
                INSERT INTO reservation (ReservationID, UserID, BookID, ReservationDate, Status)
                VALUES (%s, %s, %s, NOW(), 'Active')
            """
            
            result = db.execute_query(insert_query, (reservation_id, user_id, book_id))
            
            if result:
                return {
                    'success': True,
                    'message': 'Book reserved successfully',
                    'reservation_id': reservation_id
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to create reservation'
                }
                
        except Exception as e:
            logging.error(f"Error reserving book: {e}")
            return {
                'success': False,
                'message': 'An error occurred while reserving the book'
            }
    
    @staticmethod
    def get_user_reservations(user_id):
        try:
            db = DatabaseConnection()
            
            query = """
                SELECT r.ReservationID, r.BookID, r.ReservationDate, r.Status,
                       b.Title, b.Author, b.ISBN
                FROM reservation r
                JOIN book b ON r.BookID = b.BookID
                WHERE r.UserID = %s
                ORDER BY r.ReservationDate DESC
            """
            
            reservations = db.execute_query(query, (user_id,))
            return reservations or []
            
        except Exception as e:
            logging.error(f"Error getting user reservations: {e}")
            return []
    
    @staticmethod
    def cancel_reservation(reservation_id, user_id):
        try:
            db = DatabaseConnection()
            
            update_query = """
                UPDATE reservation 
                SET Status = 'Cancelled', CancellationDate = NOW()
                WHERE ReservationID = %s AND UserID = %s
            """
            
            result = db.execute_query(update_query, (reservation_id, user_id))
            
            if result and result > 0:
                return {
                    'success': True,
                    'message': 'Reservation cancelled successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to cancel reservation'
                }
                
        except Exception as e:
            logging.error(f"Error cancelling reservation: {e}")
            return {
                'success': False,
                'message': 'An error occurred while cancelling the reservation'
            }
    
    @staticmethod
    def get_all_reservations():
        try:
            db = DatabaseConnection()
            
            query = """
                SELECT r.ReservationID, r.UserID, r.BookID, r.ReservationDate, r.Status,
                       u.Name as user_name, u.Email as user_email,
                       b.Title, b.Author, b.ISBN
                FROM reservation r
                JOIN users u ON r.UserID = u.UserID
                JOIN book b ON r.BookID = b.BookID
                ORDER BY r.ReservationDate DESC
            """
            
            reservations = db.execute_query(query)
            return reservations or []
            
        except Exception as e:
            logging.error(f"Error getting all reservations: {e}")
            return []
