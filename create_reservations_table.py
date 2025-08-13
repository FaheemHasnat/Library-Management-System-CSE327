from app.utils.database import Database

conn = Database.get_connection()
cursor = conn.cursor()

create_book_reservations_sql = """
CREATE TABLE IF NOT EXISTS book_reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    reservation_date DATE NOT NULL,
    expiry_date DATE DEFAULT (DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
    status ENUM('Active', 'Fulfilled', 'Cancelled', 'Expired') DEFAULT 'Active',
    notes TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(UserID) ON DELETE CASCADE
)
"""

try:
    cursor.execute(create_book_reservations_sql)
    conn.commit()
    print("book_reservations table created successfully")
except Exception as e:
    print(f"Error creating table: {e}")

conn.close()
