from app.models.issued_book import IssuedBook

print("Testing updated IssuedBook queries...")

try:
    issued_books = IssuedBook.get_all_issued_books()
    print(f"✅ Issued books found: {len(issued_books)}")
    
    if issued_books:
        print("Sample issued book:")
        for key, value in issued_books[0].items():
            print(f"  {key}: {value}")
    
    students = IssuedBook.get_students()
    print(f"✅ Students found: {len(students)}")
    
    available_books = IssuedBook.get_available_books()
    print(f"✅ Available books found: {len(available_books)}")
    
    print("✅ All functions working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
