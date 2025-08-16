import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.issued_book import IssuedBook


def test_student_fines():
    print("Testing Student Fines Functionality...")
    
    try:
        students = IssuedBook.get_students()
        if students:
            sample_student = students[0]
            user_id = sample_student['UserID']
            student_name = sample_student['student_name']
            
            total_fines = IssuedBook.get_student_fines(user_id)
            print(f"Student: {student_name}")
            print(f"Total outstanding fines: {total_fines}")
            
            fine_history = IssuedBook.get_student_fine_history(user_id)
            print(f"Fine history records: {len(fine_history)}")
            
            if fine_history:
                print("Sample fine record:")
                sample = fine_history[0]
                print(f"  Book: {sample.get('book_title')}")
                print(f"  Fine Amount: {sample.get('Fine')}")
                print(f"  Return Date: {sample.get('ReturnDate')}")
        
        print("Student fines test completed!")
        
    except Exception as e:
        print(f"Error in student fines test: {e}")


if __name__ == "__main__":
    test_student_fines()
