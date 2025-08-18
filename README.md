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
```

## Database Schema

### Tables
- `users`: User accounts (Admin, Librarian, Student)
- `books`: Book catalog with availability status
- `book_reservations`: Book reservation tracking

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure database in `config.py`

3. Run the application:
   ```
   python app.py
   ```

## Default Accounts

- **Admin**: admin@lms.com / admin123
- **Librarian**: librarian@lms.com / lib123  
- **Student**: student@lms.com / student123

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (no frameworks)
- **Database**: MySQL
- **Architecture**: MVC Pattern
- **Standards**: PEP 8 compliant
