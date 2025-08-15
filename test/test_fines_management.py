from app.models.issued_book import IssuedBook

print("=== Testing Fines Management Functionality ===")

print("\n1. Testing get_users_with_fines():")
users_with_fines = IssuedBook.get_users_with_fines()
if users_with_fines:
    print(f"Found {len(users_with_fines)} users with fines:")
    for fine in users_with_fines:
        print(f"  - {fine['student_name']}: {fine['Fine']} Taka for '{fine['book_title']}'")
else:
    print("No users with fines found")

print("\n2. Testing get_fines_summary():")
summary = IssuedBook.get_fines_summary()
print(f"Summary: {summary}")

print("\n=== Test Complete ===")
