# Library Management System

A streamlined library management system built with Python Flask following MVC architecture.

## Features

### Admin Features
- Member management (add, edit, delete members)
- View all members with role-based filtering
- Student and librarian account management

### Librarian Features
- Book issue to students
- Book return processing with fine calculation
- View issued books status

### Authentication
- Secure login/logout system
- Role-based access control (Admin, Librarian)
- Session management

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure database settings in `config.py`
4. Run the application:
   ```
   python app.py
   ```

## Testing

The project includes comprehensive unit tests using pytest framework.

### Run Tests
```bash
# Run all tests
pytest test/ -v

# Run specific test file
pytest test/test_member_management.py -v

# Using the test runner script
python run_tests.py
```

### Test Coverage
- **Member Management**: Add, edit, delete, view members
- **Book Issue**: Issue books with validation and limits
- **Book Return**: Return books with fine calculation

See `test/README.md` for detailed testing documentation.

## Technology Stack

- Backend: Python Flask
- Database: MySQL
- Frontend: HTML, CSS (no frameworks)
- Architecture: MVC Pattern
- Code Standard: PEP8
- Testing: pytest, pytest-mock

## Project Structure

```
LibMS/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── run_tests.py          # Test runner script
├── pytest.ini           # Pytest configuration
├── app/
│   ├── controllers/       # Business logic
│   │   ├── auth_controller.py
│   │   ├── admin_controller.py
│   │   └── librarian_controller.py
│   ├── models/           # Data models
│   │   ├── user.py
│   │   ├── book.py
│   │   └── issued_book.py
│   ├── utils/            # Database utilities
│   └── views/            # Templates and static files
└── test/                 # Unit tests
    ├── test_member_management.py
    ├── test_book_issue.py
    ├── test_book_return.py
    └── README.md         # Testing documentation
```

## Default Login Credentials

- Admin: admin@lms.com / admin123
- Librarian: librarian@lms.com / lib123
