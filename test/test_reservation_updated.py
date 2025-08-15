from app.models.book import Book

print("Testing Updated Book Reservation Feature")
print("="*45)

print("\n1. Testing get all available books:")
books = Book.get_all_available_books()
print(f"Found {len(books)} available books")
for i, book in enumerate(books[:5], 1):
    print(f"  {i}. {book['title']} by {book['author']}")

print("\n2. Testing get all students:")
students = Book.get_all_students()
print(f"Found {len(students)} students")
for i, student in enumerate(students, 1):
    print(f"  {i}. {student['full_name']} ({student['email']})")

print("\n3. Testing multiple reservations creation:")
if books and students:
    book_ids = [books[0]['book_id'], books[1]['book_id'], books[2]['book_id']]
    student_id = students[0]['user_id']
    
    print(f"Creating reservations for books: {[book['title'] for book in books[:3]]}")
    print(f"For student: {students[0]['full_name']}")
    
    success_count = Book.create_multiple_reservations(book_ids, student_id)
    print(f"Successfully created {success_count} reservations")

print("\n4. Testing recent reservations:")
reservations = Book.get_recent_reservations()
print(f"Found {len(reservations)} recent reservations")
for i, res in enumerate(reservations[:3], 1):
    print(f"  {i}. {res['title']} - {res['full_name']} ({res['reservation_date']})")

print("\nBook reservation feature test completed successfully!")
