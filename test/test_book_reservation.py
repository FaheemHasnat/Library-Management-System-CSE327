import pytest
from unittest.mock import patch, MagicMock
from flask import session
from app import create_app
from app.controllers.librarian_controller import LibrarianController


@pytest.fixture
def app():
    app = create_app(initialize_db=False)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_books():
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
        }
    ]


@pytest.fixture
def mock_students():
    return [
        {
            'user_id': 1,
            'full_name': 'John Student',
            'email': 'john@example.com'
        },
        {
            'user_id': 2,
            'full_name': 'Jane Student',
            'email': 'jane@example.com'
        }
    ]


@pytest.fixture
def mock_reservations():
    return [
        {
            'reservation_id': 'res-001',
            'title': 'Python Programming',
            'full_name': 'John Student',
            'reservation_date': '2025-08-17'
        }
    ]


class TestBookReservation:

    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_book_reservation_page_loads_correctly(self, mock_books_filter, mock_db_query, client, mock_books, mock_students, mock_reservations):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, mock_reservations]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/book-reservation')
        assert response.status_code == 200
        assert b'Book Reservation' in response.data
        assert b'Select books and assign them to students' in response.data

    def test_book_reservation_redirects_without_login(self, client):
        response = client.get('/librarian/book-reservation')
        assert response.status_code == 302
        assert '/login' in response.location

    def test_book_reservation_denies_non_librarian_access(self, client):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'Test Admin'
            sess['user_role'] = 'Admin'
        
        response = client.get('/librarian/book-reservation')
        assert response.status_code == 302
        assert '/login' in response.location

    @patch('app.models.book.Book.get_student_reservation_count')
    @patch('app.models.book.Book.create_reservation')
    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_successful_book_reservation(self, mock_books_filter, mock_db_query, mock_create_reservation, mock_reservation_count, client, mock_books, mock_students):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, []]
        mock_reservation_count.return_value = 0
        mock_create_reservation.return_value = True
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.post('/librarian/book-reservation', data={
            'selected_books': ['book-001'],
            'student_id': '1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'All 1 book reservations created successfully' in response.data

    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_requires_book_selection(self, mock_books_filter, mock_db_query, client, mock_books, mock_students):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, []]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.post('/librarian/book-reservation', data={
            'student_id': '1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please select at least one book' in response.data

    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_requires_student_selection(self, mock_books_filter, mock_db_query, client, mock_books, mock_students):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, []]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.post('/librarian/book-reservation', data={
            'selected_books': ['book-001']
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please select a student' in response.data

    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_limits_book_selection(self, mock_books_filter, mock_db_query, client, mock_books, mock_students):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, []]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.post('/librarian/book-reservation', data={
            'selected_books': ['book-001', 'book-002', 'book-003', 'book-004'],
            'student_id': '1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'You can select maximum 3 books at a time' in response.data

    @patch('app.models.book.Book.get_student_reservation_count')
    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_enforces_student_limit(self, mock_books_filter, mock_db_query, mock_reservation_count, client, mock_books, mock_students):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, []]
        mock_reservation_count.return_value = 2
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.post('/librarian/book-reservation', data={
            'selected_books': ['book-001', 'book-002'],
            'student_id': '1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Student already has 2 reservations. Cannot reserve 2 more books (limit: 3)' in response.data

    @patch('app.models.book.Book.get_student_reservation_count')
    @patch('app.models.book.Book.create_reservation')
    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_handles_limit_exceeded_error(self, mock_books_filter, mock_db_query, mock_create_reservation, mock_reservation_count, client, mock_books, mock_students):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, []]
        mock_reservation_count.return_value = 0
        mock_create_reservation.return_value = "limit_exceeded"
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.post('/librarian/book-reservation', data={
            'selected_books': ['book-001'],
            'student_id': '1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Student has reached the reservation limit of 3 books' in response.data

    @patch('app.models.book.Book.get_student_reservation_count')
    @patch('app.models.book.Book.create_reservation')
    @patch('app.models.book.Book.get_book_by_id')
    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_handles_partial_success(self, mock_books_filter, mock_db_query, mock_get_book, mock_create_reservation, mock_reservation_count, client, mock_books, mock_students):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, []]
        mock_reservation_count.return_value = 0
        mock_create_reservation.side_effect = [True, False]
        mock_get_book.return_value = {'title': 'Web Development'}
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.post('/librarian/book-reservation', data={
            'selected_books': ['book-001', 'book-002'],
            'student_id': '1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'1 out of 2 reservations created successfully' in response.data

    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_displays_available_books(self, mock_books_filter, mock_db_query, client, mock_books, mock_students, mock_reservations):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, mock_reservations]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/book-reservation')
        assert response.status_code == 200
        assert b'Python Programming' in response.data
        assert b'Web Development' in response.data

    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_displays_students_list(self, mock_books_filter, mock_db_query, client, mock_books, mock_students, mock_reservations):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, mock_reservations]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/book-reservation')
        assert response.status_code == 200
        assert b'John Student' in response.data
        assert b'Jane Student' in response.data

    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_displays_recent_reservations(self, mock_books_filter, mock_db_query, client, mock_books, mock_students, mock_reservations):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, mock_reservations]
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/book-reservation')
        assert response.status_code == 200
        assert b'Recent Reservations' in response.data

    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_handles_database_error(self, mock_books_filter, mock_db_query, client):
        mock_books_filter.return_value = []
        mock_db_query.side_effect = Exception("Database error")
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.get('/librarian/book-reservation')
        assert response.status_code == 200
        assert b'Book Reservation' in response.data

    @patch('app.models.book.Book.get_student_reservation_count')
    @patch('app.models.book.Book.create_reservation')
    @patch('app.utils.database.Database.execute_query')
    @patch('app.models.book.Book.get_all_books_with_filter')
    def test_reservation_creation_failure(self, mock_books_filter, mock_db_query, mock_create_reservation, mock_reservation_count, client, mock_books, mock_students):
        mock_books_filter.return_value = mock_books
        mock_db_query.side_effect = [mock_students, []]
        mock_reservation_count.return_value = 0
        mock_create_reservation.return_value = False
        
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Test Librarian'
            sess['user_role'] = 'Librarian'
        
        response = client.post('/librarian/book-reservation', data={
            'selected_books': ['book-001'],
            'student_id': '1'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Failed to create reservations' in response.data
