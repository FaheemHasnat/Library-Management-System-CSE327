# Library Management System - Test Suite

This directory contains comprehensive unit tests for the Library Management System features:
- Login functionality
- Signup functionality  
- Book Status (Admin, Librarian, Student dashboards)

## Running Tests

### Install Test Dependencies
```bash
pip install -r test/requirements.txt
```

### Run All Tests
```bash
pytest test/
```

### Run Specific Test Files
```bash
# Test login functionality
pytest test/test_login.py

# Test signup functionality
pytest test/test_signup.py

# Test book status functionality
pytest test/test_book_status.py
```

### Run Tests with Coverage
```bash
pytest test/ --cov=app --cov-report=html
```

### Run Tests with Verbose Output
```bash
pytest test/ -v
```

## Test Structure

### test_login.py
- Tests GET and POST requests for login
- Validates authentication with valid/invalid credentials
- Tests role-based redirections (Admin, Librarian, Student)
- Handles edge cases and database errors

### test_signup.py
- Tests GET and POST requests for signup
- Validates form data and field requirements
- Tests password validation and confirmation
- Checks email uniqueness and role validation
- Handles user creation success/failure scenarios

### test_book_status.py
- Tests book status functionality for all three dashboards
- Validates role-based access control
- Tests book data retrieval and display
- Includes model-level tests for book operations
- Tests filtering and statistics calculations

### conftest.py
- Contains shared test fixtures and configuration
- Provides mock database and application setup

## Test Coverage

The test suite covers:
- ✅ User authentication and authorization
- ✅ Form validation and error handling
- ✅ Database operations (mocked)
- ✅ Role-based access control
- ✅ Edge cases and error scenarios
- ✅ Session management
- ✅ Book data operations and filtering

## Mocking Strategy

Tests use `unittest.mock` to:
- Mock Flask request/response objects
- Mock database operations
- Mock external dependencies
- Isolate units under test

This ensures tests run fast and don't require actual database connections.
