# Test Suite for Library Management System

This directory contains comprehensive unit tests for the Library Management System (LIBMS) project.

## Test Structure

```
test/
├── __init__.py                 # Makes test directory a Python package
├── conftest.py                 # Shared pytest configuration and fixtures
├── test_member_management.py   # Tests for admin member management functionality
├── test_book_issue.py         # Tests for librarian book issue functionality
└── test_book_return.py        # Tests for librarian book return functionality
```

## Test Coverage

### 1. Member Management Tests (`test_member_management.py`)
- **Add Member**: Test successful member addition, validation errors, duplicate emails
- **Edit Member**: Test member search, update operations, field validations
- **Delete Member**: Test member deletion, error handling
- **View Members**: Test member listing, role-based counting
- **Access Control**: Test admin access validation

### 2. Book Issue Tests (`test_book_issue.py`)
- **Issue Book**: Test successful book issuing, student eligibility checks
- **Validation**: Test borrowing limits (max 3 books), book availability
- **Error Handling**: Test missing parameters, database failures
- **Data Retrieval**: Test getting available books, students, issued books

### 3. Book Return Tests (`test_book_return.py`)
- **Return Book**: Test successful book returns, status updates
- **Fine Calculation**: Test late return fine calculations (10 Taka per day)
- **Validation**: Test return date validation, issued book verification
- **Transaction History**: Test transaction logging and fine tracking

## Running Tests

### Prerequisites
```bash
pip install pytest pytest-mock
```

### Run All Tests
```bash
# From project root directory
pytest test/ -v

# Using Python module
python -m pytest test/ -v

# Using the test runner script
python run_tests.py
```

### Run Specific Test Files
```bash
# Member management tests only
pytest test/test_member_management.py -v

# Book issue tests only
pytest test/test_book_issue.py -v

# Book return tests only
pytest test/test_book_return.py -v
```

### Run Specific Test Methods
```bash
# Run specific test method
pytest test/test_member_management.py::TestMemberManagement::test_add_member_success -v

# Run all tests in a class
pytest test/test_book_issue.py::TestBookIssue -v
```

## Test Features

### Mocking Strategy
- **Database Mocking**: All database calls are mocked to avoid dependencies
- **Session Mocking**: Flask session is mocked for authentication tests
- **Form Data Mocking**: Request form data is mocked for POST request tests
- **External Dependencies**: All external dependencies (flash, redirect, render_template) are mocked

### Test Types
- **Positive Tests**: Test successful operations with valid data
- **Negative Tests**: Test error handling with invalid data
- **Edge Cases**: Test boundary conditions and special scenarios
- **Access Control**: Test authentication and authorization

### Assertions
- Uses simple `assert` statements instead of unittest-style methods
- Clear, readable test assertions
- Comprehensive coverage of return values and side effects

## Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
```

### Fixtures (conftest.py)
- `app`: Flask application instance for testing
- `client`: Test client for HTTP requests
- `mock_db`: Mock database for isolated testing
- `setup_test_environment`: Environment setup for each test

## Example Test Output

```
test/test_member_management.py::TestMemberManagement::test_add_member_success PASSED
test/test_member_management.py::TestMemberManagement::test_add_member_missing_fields PASSED
test/test_book_issue.py::TestBookIssue::test_book_issue_post_success PASSED
test/test_book_return.py::TestBookReturn::test_book_return_post_success_no_fine PASSED

======================= 45 passed in 2.34s =======================
```

## Best Practices

1. **Isolation**: Each test is independent and doesn't rely on external state
2. **Mocking**: All external dependencies are mocked for reliable testing
3. **Clear Naming**: Test names clearly describe what is being tested
4. **Comprehensive Coverage**: Both success and failure scenarios are tested
5. **Fast Execution**: Tests run quickly without database dependencies

## Continuous Integration

These tests are designed to be easily integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest test/ -v --tb=short
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the project root is in Python path
2. **Missing Dependencies**: Install pytest and pytest-mock
3. **Path Issues**: Run tests from the project root directory

### Debug Mode
```bash
# Run with more verbose output
pytest test/ -vv --tb=long

# Run with print statements visible
pytest test/ -v -s

# Run specific failing test
pytest test/test_member_management.py::TestMemberManagement::test_specific_method -vv
```
