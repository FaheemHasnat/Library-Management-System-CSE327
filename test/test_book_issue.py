from app.models.issued_book import IssuedBook
from app.models.book import Book

print("Testing book issuing functionality...")

try:
    available_books = IssuedBook.get_available_books()
    print(f"Available books found: {len(available_books)}")
    
    students = IssuedBook.get_students()
    print(f"Students found: {len(students)}")
    
    issued_books = IssuedBook.get_all_issued_books()
    print(f"Currently issued books: {len(issued_books)}")
    
    print("All functions are working correctly!")
    
except Exception as e:
    print(f"Error: {e}")
