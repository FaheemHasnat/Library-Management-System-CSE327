import pytest
import sys
import os

# Add the parent directory to the Python path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope="session")
def app_config():
    """Configuration for test app"""
    return {
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False
    }


@pytest.fixture(autouse=True)
def mock_database_initialization():
    """Mock database initialization to prevent actual database calls during testing"""
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("app.utils.db_initializer.DatabaseInitializer.initialize_all", lambda: True)
        yield


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        'admin': {
            'user_id': 1,
            'name': 'Test Admin',
            'email': 'admin@test.com',
            'role': 'Admin'
        },
        'librarian': {
            'user_id': 2,
            'name': 'Test Librarian',
            'email': 'librarian@test.com',
            'role': 'Librarian'
        },
        'student': {
            'user_id': 3,
            'name': 'Test Student',
            'email': 'student@test.com',
            'role': 'Student'
        }
    }


@pytest.fixture
def sample_book_data():
    """Sample book data for testing"""
    return [
        {
            'book_id': 'book-001',
            'title': 'Python Programming',
            'author': 'John Smith',
            'subject': 'Computer Science',
            'isbn': '978-1234567890',
            'status': 'Available'
        },
        {
            'book_id': 'book-002',
            'title': 'Web Development',
            'author': 'Jane Doe',
            'subject': 'Computer Science',
            'isbn': '978-0987654321',
            'status': 'Available'
        },
        {
            'book_id': 'book-003',
            'title': 'Database Design',
            'author': 'Bob Johnson',
            'subject': 'Computer Science',
            'isbn': '978-1122334455',
            'status': 'Reserved'
        }
    ]
