from app.models.issued_book import IssuedBook
from datetime import datetime

print("=== Testing Book Return with Transaction Logging ===")

issued_books = IssuedBook.get_all_issued_books()
if issued_books:
    print(f"Found {len(issued_books)} issued books")
    
    test_book = issued_books[0]
    print(f"\nTesting return for:")
    print(f"  Book: {test_book['title']}")
    print(f"  Student: {test_book['student_name']}")
    print(f"  Issue Date: {test_book['issue_date']}")
    print(f"  Due Date: {test_book['due_date']}")
    
    return_date_str = "2025-08-25"
    print(f"  Return Date: {return_date_str}")
    
    result = IssuedBook.return_book(test_book['UserID'], test_book['book_id'], return_date_str)
    
    if result and isinstance(result, dict):
        print(f"\n✅ Return processed successfully")
        print(f"  Fine Amount: {result.get('fine', 0)} Taka")
        if result.get('fine', 0) > 0:
            print("  💰 Late return fine applied")
        else:
            print("  ✅ No fine - returned on time")
    else:
        print(f"\n❌ Return failed: {result}")
        
else:
    print("No issued books found for testing")

print("\n=== Test Complete ===")
