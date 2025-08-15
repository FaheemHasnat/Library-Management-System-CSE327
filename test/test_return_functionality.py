from app.models.issued_book import IssuedBook
from datetime import datetime

print("=== Testing Book Return Functionality ===")

issued_books = IssuedBook.get_all_issued_books()
if issued_books:
    test_book = issued_books[0]
    print(f"Testing return for book issued on {test_book['issue_date']} with due date {test_book['due_date']}")
    
    return_date = "2025-08-15"
    print(f"Return date: {return_date}")
    
    expected_days_late = (datetime.strptime(return_date, '%Y-%m-%d').date() - test_book['due_date']).days
    expected_fine = expected_days_late * 10 if expected_days_late > 0 else 0
    print(f"Expected fine: {expected_fine} Taka ({expected_days_late} days late)")
    
    result = IssuedBook.return_book(test_book['UserID'], test_book['book_id'], return_date)
    
    if result and isinstance(result, dict):
        print(f"✅ Return successful!")
        print(f"Fine charged: {result.get('fine', 0)} Taka")
    else:
        print(f"❌ Return failed: {result}")
        
else:
    print("❌ No issued books found")

print("=== Test Complete ===")
