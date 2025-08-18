# Library Management System

A streamlined Flask-based Library Management System focusing on essential dashboard functionality and book reservations.

## Features

### Three Dashboard System
- **Admin Dashboard**: Overview and management interface for administrators
- **Librarian Dashboard**: Access to book reservation management 
- **Student Dashboard**: Personal dashboard with reservation tracking

### Book Reservation System
- Librarians can create book reservations for students
- Maximum 3 reservations per student
- Real-time availability checking
- Reservation tracking and management

## Project Structure

```
app.py                  # Application entry point
config.py              # Configuration settings
requirements.txt       # Python dependencies
test_setup.py          # Test setup verification script
pytest.ini             # Pytest configuration

app/
├── __init__.py        # Application factory
├── controllers/       # Request handlers
│   ├── auth_controller.py      # Authentication logic
│   ├── admin_controller.py     # Admin dashboard
│   ├── librarian_controller.py # Librarian dashboard & reservations
│   └── student_controller.py   # Student dashboard
├── models/           # Data models
│   ├── user.py       # User management
│   └── book.py       # Book and reservation management
├── utils/            # Utilities
│   ├── database.py   # Database connection
│   └── db_initializer.py # Database setup
└── views/            # Templates and static files
    ├── templates/    # HTML templates
    │   ├── base.html
    │   ├── auth/     # Login/signup pages
    │   ├── dashboard/ # Dashboard templates
    │   └── librarian/ # Book reservation template
    └── static/       # CSS, JS, images

test/                   # Unit test suite
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_admin_dashboard.py  # Admin dashboard tests
├── test_librarian_dashboard.py  # Librarian dashboard tests
├── test_student_dashboard.py    # Student dashboard tests
└── test_book_reservation.py     # Book reservation functionality tests
```

## Database Schema

### Tables
- `users`: User accounts (Admin, Librarian, Student)
- `books`: Book catalog with availability status
- `book_reservations`: Book reservation tracking

## Setup

### Prerequisites
Make sure you have Python 3.7+ installed.

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Library-Management-System
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure database in `config.py`

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at `http://localhost:5000`

## Testing

### Quick Setup Verification
Run the setup verification script first:
```bash
python test_setup.py
```

### Running All Tests
```bash
python -m pytest test/ -v
```

### Running Specific Test Files
```bash
# Admin dashboard tests only
python -m pytest test/test_admin_dashboard.py -v

# Librarian dashboard tests only  
python -m pytest test/test_librarian_dashboard.py -v

# Student dashboard tests only
python -m pytest test/test_student_dashboard.py -v

# Book reservation tests only
python -m pytest test/test_book_reservation.py -v
```

### Running Specific Test Functions
```bash
# Test a specific function
python -m pytest test/test_book_reservation.py::TestBookReservation::test_reserve_book_success -v
```

### Test Features
- **Mocking**: All tests use mocked database connections (no real database required)
- **Flask Test Client**: Simulates HTTP requests for testing
- **Session Mocking**: Tests authentication and session handling
- **Isolated Tests**: Each test runs independently with fresh mock data
- **Fast Execution**: All tests complete in under 10 seconds

### Test Coverage Areas
1. **Dashboard Rendering**: Tests that all dashboards render correctly with proper data
2. **Authentication**: Tests login requirements and session handling
3. **Book Reservation**: Tests reservation logic including limits and validation
4. **Error Handling**: Tests proper error responses and edge cases

## Default Accounts

- **Admin**: admin@lms.com / admin123
- **Librarian**: librarian@lms.com / lib123  
- **Student**: student@lms.com / student123

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (no frameworks)
- **Database**: MySQL
- **Testing**: pytest, pytest-mock
- **Architecture**: MVC Pattern
- **Standards**: PEP 8 compliant

## Dependencies

### Production Dependencies
- `flask==3.1.1` - Web framework
- `mysql-connector-python==8.3.0` - MySQL database connector

### Development Dependencies
- `pytest==7.4.0` - Testing framework
- `pytest-mock==3.11.1` - Mocking capabilities

## Development Notes

This is a streamlined version of a library management system that focuses on:
- Core dashboard functionality for three user types
- Book reservation system with business logic
- Clean MVC architecture
- Comprehensive unit test coverage
- No unnecessary features or complexity

The system has been cleaned up to remove unused functionality and focus on the essential features that demonstrate a working library management system.
