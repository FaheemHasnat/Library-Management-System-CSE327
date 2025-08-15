from app.models.issued_book import IssuedBook

print("=== Testing Book Borrowing Limit Validation ===")

students = IssuedBook.get_students()
books = IssuedBook.get_available_books()

if students and books:
    test_student = students[0]
    test_book = books[0]
    
    print(f"\nTesting with student: {test_student['student_name']} (ID: {test_student['UserID']})")
    print(f"Testing with book: {test_book['title']} (ID: {test_book['book_id']})")
    
    current_count = IssuedBook.get_student_borrowed_count(test_student['UserID'])
    print(f"Current borrowed books count: {current_count}")
    
    if current_count >= 3:
        print("✅ Student already has 3+ books - testing limit validation")
        result = IssuedBook.issue_book(test_student['UserID'], test_book['book_id'])
        if result == "limit_exceeded":
            print("✅ PASS: Correctly blocked issuing due to 3-book limit")
        else:
            print(f"❌ FAIL: Expected 'limit_exceeded', got: {result}")
    else:
        print(f"Student has {current_count} books - can still borrow more")
        
        if current_count < 3:
            print("Testing normal book issue...")
            result = IssuedBook.issue_book(test_student['UserID'], test_book['book_id'])
            if result == True:
                print("✅ Book issued successfully")
                new_count = IssuedBook.get_student_borrowed_count(test_student['UserID'])
                print(f"New borrowed count: {new_count}")
            else:
                print(f"Issue result: {result}")
else:
    print("❌ No students or books available for testing")

print("\n=== Test Complete ===")
