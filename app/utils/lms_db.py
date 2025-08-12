import mysql.connector
from mysql.connector import Error
from config import Config
import logging


class DatabaseConnection:
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**Config.get_db_config())
            self.cursor = self.connection.cursor(dictionary=True, buffered=True)
            logging.info("Database connection established successfully")
            return True
        except Error as e:
            logging.error(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logging.info("Database connection closed")
        except Error as e:
            logging.error(f"Error closing database connection: {e}")
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            self.cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                if fetch_one:
                    return self.cursor.fetchone()
                elif fetch_all:
                    return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
                
        except Error as e:
            logging.error(f"Database query error: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def execute_transaction(self, queries_with_params):
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            self.connection.start_transaction()
            
            for query, params in queries_with_params:
                self.cursor.execute(query, params or ())
            
            self.connection.commit()
            return True
            
        except Error as e:
            logging.error(f"Transaction error: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


db = DatabaseConnection()
