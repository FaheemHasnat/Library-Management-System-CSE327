import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def pytest_configure():
    """Configure pytest settings."""
    pytest.test_db_name = "lms_test"


@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture(scope="session")
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def mock_database():
    """Mock database fixture for tests."""
    from unittest.mock import patch
    with patch('app.utils.database.Database') as mock_db:
        yield mock_db
