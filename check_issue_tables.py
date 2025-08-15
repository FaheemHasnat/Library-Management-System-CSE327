from app.utils.database import Database

conn = Database.get_connection()
cursor = conn.cursor()

print("Checking available tables:")
cursor.execute('SHOW TABLES')
tables = cursor.fetchall()
for table in tables:
    print(f"  {table[0]}")

print("\nChecking for issued_books table:")
try:
    cursor.execute('SELECT COUNT(*) FROM issued_books')
    count = cursor.fetchone()[0]
    print(f"  issued_books table exists with {count} records")
except Exception as e:
    print(f"  issued_books table error: {e}")

print("\nChecking for book_issues table:")
try:
    cursor.execute('SELECT COUNT(*) FROM book_issues')
    count = cursor.fetchone()[0]
    print(f"  book_issues table exists with {count} records")
except Exception as e:
    print(f"  book_issues table error: {e}")

conn.close()
