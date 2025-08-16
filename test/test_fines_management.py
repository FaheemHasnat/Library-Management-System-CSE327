import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.issued_book import IssuedBook


def test_fines_management():
    print("Testing Fines Management System...")
    
    try:
        fines_summary = IssuedBook.get_fines_summary()
        print(f"Total outstanding fines: {fines_summary['total_outstanding']}")
        print(f"Total fine records: {fines_summary['total_fines']}")
        print(f"Collected today: {fines_summary['collected_today']}")
        
        users_with_fines = IssuedBook.get_users_with_fines()
        print(f"Users with fines: {len(users_with_fines)}")
        
        if users_with_fines:
            print("Sample fine record:")
            sample = users_with_fines[0]
            print(f"  Student: {sample.get('student_name')}")
            print(f"  Book: {sample.get('book_title')}")
            print(f"  Fine Amount: {sample.get('Fine')}")
            print(f"  Return Date: {sample.get('ReturnDate')}")
        
        print("Fines management test completed!")
        
    except Exception as e:
        print(f"Error in fines management test: {e}")


if __name__ == "__main__":
    test_fines_management()
