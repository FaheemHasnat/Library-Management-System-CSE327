from app.utils.database import Database

print("=== DEBUGGING ISSUED BOOKS QUERY ===")

conn = Database.get_connection()
if not conn:
    print("❌ Cannot connect to database")
    exit()

cursor = conn.cursor()

print("\n1. Checking table structure for issued_books:")
try:
    cursor.execute('DESCRIBE issued_books')
    for row in cursor.fetchall():
        print(f"   {row}")
except Exception as e:
    print(f"   Error describing issued_books: {e}")

print("\n2. Checking all records in issued_books:")
try:
    cursor.execute('SELECT * FROM issued_books LIMIT 5')
    records = cursor.fetchall()
    if records:
        for record in records:
            print(f"   {record}")
    else:
        print("   No records found in issued_books table")
except Exception as e:
    print(f"   Error querying issued_books: {e}")

print("\n3. Testing the current query:")
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
WHERE ib.return_date IS NULL
ORDER BY ib.issue_date DESC
"""

try:
    cursor.execute(query)
    results = cursor.fetchall()
    print(f"   Query returned {len(results)} results")
    for result in results:
        print(f"   {result}")
except Exception as e:
    print(f"   Error executing query: {e}")

print("\n4. Checking records without return_date filter:")
try:
    cursor.execute('SELECT COUNT(*) FROM issued_books')
    total = cursor.fetchone()[0]
    print(f"   Total records in issued_books: {total}")
    
    cursor.execute('SELECT COUNT(*) FROM issued_books WHERE return_date IS NULL')
    active = cursor.fetchone()[0]
    print(f"   Records with return_date IS NULL: {active}")
    
    cursor.execute('SELECT COUNT(*) FROM issued_books WHERE return_date IS NOT NULL')
    returned = cursor.fetchone()[0]
    print(f"   Records with return_date IS NOT NULL: {returned}")
except Exception as e:
    print(f"   Error counting records: {e}")

conn.close()
