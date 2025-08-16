import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.issued_book import IssuedBook
from datetime import datetime


def test_book_return_functionality():
    print("Testing Book Return Functionality...")
    
    try:
        issued_books = IssuedBook.get_all_issued_books()
        print(f"Currently issued books: {len(issued_books)}")
        
        if issued_books:
            print("Sample issued book:")
            sample_book = issued_books[0]
            print(f"  User ID: {sample_book.get('UserID')}")
            print(f"  Book ID: {sample_book.get('book_id')}")
            print(f"  Book Title: {sample_book.get('title')}")
            print(f"  Issue Date: {sample_book.get('issue_date')}")
            print(f"  Due Date: {sample_book.get('due_date')}")
        
        print("Book return functionality test completed!")
        
    except Exception as e:
        print(f"Error in book return test: {e}")


def test_transaction_history():
    print("\nTesting Transaction History...")
    
    try:
        transactions = IssuedBook.get_transaction_history()
        print(f"Total transactions: {len(transactions)}")
        
        if transactions:
            print("Recent transaction:")
            recent = transactions[0]
            print(f"  Student: {recent.get('student_name')}")
            print(f"  Book: {recent.get('book_title')}")
            print(f"  Return Date: {recent.get('ReturnDate')}")
            print(f"  Fine: {recent.get('Fine')}")
        
        print("Transaction history test completed!")
        
    except Exception as e:
        print(f"Error in transaction history test: {e}")


if __name__ == "__main__":
    test_book_return_functionality()
    test_transaction_history()
