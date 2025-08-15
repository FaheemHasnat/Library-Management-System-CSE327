from app.models.book import Book

print("Testing Book Reservation Feature")
print("="*40)

print("\n1. Testing search functionality:")
books = Book.search_available_books("python")
print(f"Found {len(books)} books matching 'python'")
for book in books:
    print(f"  - {book['title']} by {book['author']}")

print("\n2. Testing user lookup:")
user = Book.get_user_by_email("student1@lms.com")
if user:
    print(f"Found user: {user['full_name']} ({user['email']})")
else:
    print("User not found")

print("\n3. Testing reservation creation:")
if books and user:
    result = Book.create_reservation(books[0]['book_id'], user['user_id'])
    print(f"Reservation created: {result}")

print("\n4. Testing recent reservations:")
reservations = Book.get_recent_reservations()
print(f"Found {len(reservations)} recent reservations")
for res in reservations[:3]:
    print(f"  - {res['title']} reserved by {res['full_name']} on {res['reservation_date']}")

print("\nBook reservation feature test completed!")
