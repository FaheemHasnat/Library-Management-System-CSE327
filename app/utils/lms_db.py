import mysql.connector
from mysql.connector import Error
<<<<<<< HEAD
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
=======
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
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
        except Error as e:
            logging.error(f"Error closing database connection: {e}")
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        try:
<<<<<<< HEAD
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
            
=======
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
                
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
        except Error as e:
            logging.error(f"Database query error: {e}")
            if self.connection:
                self.connection.rollback()
            return None
<<<<<<< HEAD
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
=======
    
    def execute_transaction(self, queries_with_params):
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            self.connection.start_transaction()
            
            for query, params in queries_with_params:
                self.cursor.execute(query, params or ())
            
            self.connection.commit()
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c
            return True
            
        except Error as e:
            logging.error(f"Transaction error: {e}")
            if self.connection:
                self.connection.rollback()
            return False
<<<<<<< HEAD
        finally:
            self.disconnect()
=======
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
>>>>>>> fc25a9493b7ee3c6b8bbf27d715e8cfdebbc906c


db = DatabaseConnection()
