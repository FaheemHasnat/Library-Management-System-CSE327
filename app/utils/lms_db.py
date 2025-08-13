import mysql.connector
from mysql.connector import Error
import logging
from config import Config


class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.db_config = Config.get_db_config()
    
    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.db_config)
                logging.info("MySQL connection established")
            return self.connection
        except Error as e:
            logging.error(f"Database connection error: {e}")
            return None
    
    def disconnect(self):
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                self.connection = None
                logging.info("MySQL connection closed")
        except Error as e:
            logging.error(f"Error closing database connection: {e}")
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        try:
            connection = self.connect()
            if not connection:
                return None
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                if fetch_one:
                    result = cursor.fetchone()
                elif fetch_all:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchall()
            else:
                connection.commit()
                result = cursor.rowcount
            
            cursor.close()
            return result
            
        except Error as e:
            logging.error(f"Database query error: {e}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            self.disconnect()
    
    def execute_single(self, query, params=None):
        return self.execute_query(query, params, fetch_one=True, fetch_all=False)
    
    def execute_transaction(self, queries_with_params):
        try:
            connection = self.connect()
            if not connection:
                return False
            
            connection.start_transaction()
            cursor = connection.cursor()
            
            for query, params in queries_with_params:
                cursor.execute(query, params or ())
            
            connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            logging.error(f"Transaction error: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            self.disconnect()


db = DatabaseConnection()
