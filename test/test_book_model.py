import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.book import Book


def test_book_statistics():
    print("Testing Book Model Statistics...")
    
    try:
        stats = Book.get_library_stats()
        print(f"Total books: {stats['total_books']}")
        print(f"Available books: {stats['available_books']}")
        print(f"Issued books: {stats['issued_books']}")
        print(f"Overdue books: {stats['overdue_books']}")
        print(f"Reservations: {stats['reservations']}")
        print(f"Availability percentage: {stats['availability_percentage']}%")
        
        print("Book statistics test completed successfully!")
        
    except Exception as e:
        print(f"Error in book statistics test: {e}")


def test_book_operations():
    print("\nTesting Book Operations...")
    
    try:
        books = Book.get_all_books()
        print(f"Total books retrieved: {len(books)}")
        
        available_books = Book.get_all_available_books()
        print(f"Available books: {len(available_books)}")
        
        students = Book.get_all_students()
        print(f"Students found: {len(students)}")
        
        print("Book operations test completed successfully!")
        
    except Exception as e:
        print(f"Error in book operations test: {e}")


if __name__ == "__main__":
    test_book_statistics()
    test_book_operations()
