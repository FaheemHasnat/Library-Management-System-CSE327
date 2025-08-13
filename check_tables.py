from app.utils.database import Database

conn = Database.get_connection()
cursor = conn.cursor()

cursor.execute('DESCRIBE users')
print('Users table structure:')
for row in cursor.fetchall():
    print(row)

cursor.execute('DESCRIBE books')
print('\nBooks table structure:')
for row in cursor.fetchall():
    print(row)

conn.close()
