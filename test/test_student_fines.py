from app.models.issued_book import IssuedBook

print("=== Testing Student Fines Functionality ===")

print("\n1. Testing get_student_fines():")
student_fines = IssuedBook.get_student_fines(1)
print(f"Student 1 total fines: {student_fines}")

print("\n2. Testing get_student_fine_history():")
fine_history = IssuedBook.get_student_fine_history(1)
print(f"Student 1 fine history records: {len(fine_history)}")

if fine_history:
    print("Fine history details:")
    for record in fine_history:
        print(f"  - Book: {record.get('book_title', 'Unknown')}")
        print(f"    Fine: {record.get('Fine', 0)}")
        print(f"    Return Date: {record.get('ReturnDate', 'N/A')}")
        print()
else:
    print("No fine history found for this student")

print("\n3. Testing controller import:")
try:
    from app.controllers.student_controller import StudentController
    print("StudentController imported successfully")
except Exception as e:
    print(f"Import error: {e}")

print("\nAll tests completed!")
