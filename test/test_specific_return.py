from app.models.issued_book import IssuedBook
from datetime import datetime

print("=== Testing Book Return with Test Record ===")

user_id = "17585a69-e173-4984-b117-6d4f57c488d5"
book_id = 5
return_date = "2025-08-15"

print(f"Testing return for:")
print(f"  User ID: {user_id}")
print(f"  Book ID: {book_id}")
print(f"  Return Date: {return_date}")

result = IssuedBook.return_book(user_id, book_id, return_date)

if result and isinstance(result, dict):
    print(f"✅ Return successful!")
    print(f"Fine charged: {result.get('fine', 0)} Taka")
else:
    print(f"❌ Return failed: {result}")

print("\nChecking transaction table...")
transactions = IssuedBook.get_transaction_history()
if transactions:
    latest = transactions[0]
    print(f"Latest transaction: Book {latest['BookID']} returned on {latest['ReturnDate']} with fine {latest['Fine']}")
else:
    print("No transactions found")

print("=== Test Complete ===")
