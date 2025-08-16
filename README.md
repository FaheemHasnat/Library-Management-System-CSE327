# Library Management System

A comprehensive library management system built with Python Flask following MVC architecture.

## Features

### Admin Features
- Member management (add, edit, delete)
- View all members
- Book management
- Book status monitoring
- Fines details

### Librarian Features
- Book issue and return
- Book reservation management
- Transaction history
- Fines management
- Book status monitoring
- Notification system

### Student Features
- View available books
- Book reservation
- Account status
- View borrowed books

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

## Technology Stack

- Backend: Python Flask
- Database: MySQL
- Frontend: HTML, CSS
- Architecture: MVC Pattern

## Project Structure

```
lms/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── app/
│   ├── controllers/       # Business logic
│   ├── models/           # Data models
│   ├── utils/            # Utilities
│   └── views/            # Templates and static files
└── test/                 # Test files
```
