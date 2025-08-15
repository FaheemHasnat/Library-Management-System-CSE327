from app.utils.database import Database

def fix_issued_books_table():
    connection = Database.get_connection()
    if not connection:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Drop existing table if it exists with wrong structure
        cursor.execute("DROP TABLE IF EXISTS issued_books")
        
        # Create the correct table structure
        create_table_query = """
        CREATE TABLE issued_books (
            issue_id INT AUTO_INCREMENT PRIMARY KEY,
            UserID VARCHAR(255) NOT NULL,
            book_id INT NOT NULL,
            issue_date DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES users(UserID) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        
        print("✅ issued_books table created successfully with correct structure")
        
        # Show the table structure
        cursor.execute("DESCRIBE issued_books")
        columns = cursor.fetchall()
        print("\nTable structure:")
        for col in columns:
            print(f"  {col[0]} - {col[1]} - {col[2]} - {col[3]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    fix_issued_books_table()
