import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.issued_book import IssuedBook


def test_borrowing_limit():
    print("Testing Student Borrowing Limit...")
    
    try:
        students = IssuedBook.get_students()
        if students:
            sample_student = students[0]
            user_id = sample_student['UserID']
            student_name = sample_student['student_name']
            
            borrowed_count = IssuedBook.get_student_borrowed_count(user_id)
            print(f"Student: {student_name}")
            print(f"Current borrowed books: {borrowed_count}")
            print(f"Remaining borrowing capacity: {3 - borrowed_count}")
            
            if borrowed_count >= 3:
                print("Student has reached borrowing limit")
            else:
                print("Student can borrow more books")
        
        print("Borrowing limit test completed!")
        
    except Exception as e:
        print(f"Error in borrowing limit test: {e}")


if __name__ == "__main__":
    test_borrowing_limit()
