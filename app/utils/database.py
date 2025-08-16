import mysql.connector
from mysql.connector import Error
from config import Config


class Database:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(**Config.get_db_config())
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def execute_query(query, params=None):
        connection = Database.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"Error executing query: {e}")
                return None
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return None
    
    @staticmethod
    def execute_single_query(query, params=None):
        connection = Database.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result
            except Error as e:
                print(f"Error executing query: {e}")
                return None
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return None
    
    @staticmethod
    def execute_insert_query(query, params=None):
        connection = Database.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, params)
                connection.commit()
                return cursor.lastrowid
            except Error as e:
                print(f"Error executing insert query: {e}")
                connection.rollback()
                return None
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        return None
