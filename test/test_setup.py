#!/usr/bin/env python3
"""
Simple test runner to verify our test setup
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all our modules can be imported"""
    try:
        import app
        print("✓ app module imported successfully")
        
        from app import create_app
        print("✓ create_app imported successfully")
        
        from app.models.user import User
        print("✓ User model imported successfully")
        
        from app.models.book import Book  
        print("✓ Book model imported successfully")
        
        from app.controllers.auth_controller import auth_bp
        print("✓ auth_controller imported successfully")
        
        from app.controllers.admin_controller import admin_bp
        print("✓ admin_controller imported successfully")
        
        from app.controllers.librarian_controller import librarian_bp
        print("✓ librarian_controller imported successfully")
        
        from app.controllers.student_controller import student_bp
        print("✓ student_controller imported successfully")
        
        print("\n✓ All imports successful!")
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_creation():
    """Test that the Flask app can be created"""
    try:
        import app
        flask_app = app.create_app()
        print("✓ Flask app created successfully")
        print(f"✓ App name: {flask_app.name}")
        return True
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False

def test_pytest_import():
    """Test that pytest is available"""
    try:
        import pytest
        print(f"✓ pytest imported successfully (version: {pytest.__version__})")
        return True
    except Exception as e:
        print(f"✗ pytest import error: {e}")
        return False

if __name__ == "__main__":
    print("Library Management System - Test Setup Verification")
    print("=" * 50)
    
    all_passed = True
    
    print("\n1. Testing imports...")
    all_passed &= test_imports()
    
    print("\n2. Testing app creation...")
    all_passed &= test_app_creation()
    
    print("\n3. Testing pytest availability...")
    all_passed &= test_pytest_import()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed! Your test setup is ready.")
        print("\nYou can now run the full test suite with:")
        print("python -m pytest test/ -v")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    print("\nTest files available:")
    test_files = [
        "test/test_admin_dashboard.py",
        "test/test_librarian_dashboard.py", 
        "test/test_student_dashboard.py",
        "test/test_book_reservation.py"
    ]
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"  ✓ {test_file}")
        else:
            print(f"  ✗ {test_file}")
