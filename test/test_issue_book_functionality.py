from app.models.issued_book import IssuedBook
from app.models.book import Book

print("=== Testing Issue Book Functionality ===")

print("\n1. Testing get_available_books():")
books = IssuedBook.get_available_books()
if books:
    print(f"   Found {len(books)} available books")
    print(f"   First book: {books[0]}")
else:
    print("   No available books found")

print("\n2. Testing get_students():")
students = IssuedBook.get_students()
if students:
    print(f"   Found {len(students)} students")
    print(f"   First student: {students[0]}")
else:
    print("   No students found")

print("\n3. Testing get_all_issued_books():")
issued_books = IssuedBook.get_all_issued_books()
if issued_books:
    print(f"   Found {len(issued_books)} issued books")
    print(f"   First issued book: {issued_books[0]}")
else:
    print("   No issued books found")

if books and students:
    print(f"\n4. Testing issue_book() functionality:")
    print(f"   Attempting to issue book_id: {books[0]['book_id']} to student: {students[0]['UserID']}")
    
    try:
        result = IssuedBook.issue_book(students[0]['UserID'], books[0]['book_id'])
        if result:
            print("   ✅ Book issued successfully!")
            
            print("\n5. Checking updated issued books list:")
            updated_issued = IssuedBook.get_all_issued_books()
            print(f"   Now have {len(updated_issued)} issued books")
            
        else:
            print("   ❌ Failed to issue book")
    except Exception as e:
        print(f"   ❌ Error issuing book: {e}")
else:
    print("\n4. Cannot test issue_book() - missing books or students")

print("\n=== Test Complete ===")
