import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    from app import create_app
    from config import Config
    
    class TestConfig(Config):
        TESTING = True
        WTF_CSRF_ENABLED = False
    
    app = create_app(TestConfig, initialize_db=False)
    return app


@pytest.fixture(scope="session")
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def mock_db():
    """Mock database for testing."""
    from unittest.mock import Mock
    return Mock()


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test."""
    pass
