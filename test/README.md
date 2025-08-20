# Test Suite for Library Management System

This directory contains comprehensive unit tests for the Library Management System (LIBMS) project.

## Test Structure

```
test/
├── __init__.py                         # Makes test directory a Python package
├── conftest.py                         # Shared pytest fixtures and configs
├── test_library_fine_reservation.py    # Tests for fine calculation & reservation expiry
└── test_notification_system.py         # Tests for notification system


## Test Coverage

###1.Fine & Reservation System Tests (test_library_fine_reservation.py)
 -Fine Calculation
- **No fine if returned within 14 days
- **Fine applied correctly for overdue returns (5 Taka per day)
- **Edge cases: return on exact due date, leap year dates

-Reservation Expiry
- **Reservation expires after 2 days if not collected
- **Collected within expiry → valid
- **Collected after expiry → invalid
- **Current date handling (system date > expiry)

### 2.Notification System Tests (test_notification_system.py)

-Notification Sending
- **Sends notification to correct user
- **Validates message content
- **Handles empty or invalid inputs

-Notification Queue

- **Stores pending notifications
- **Marks notifications as delivered

-Error Handling
- **Missing recipient
- **Network/delivery failure (mocked)


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
# Fine & Reservation tests only
pytest test/test_library_fine_reservation.py -v

# Notification system tests only
pytest test/test_notification_system.py -v


 ### Run Specific Test Files Methods
```bash
pytest test/test_library_fine_reservation.py::TestFineSystem::test_fine_overdue -v
pytest test/test_notification_system.py::TestNotificationSystem::test_send_notification_success -v

```

## Test Features

### Mocking Strategy
-Mocking Strategy
-**Date Mocking: datetime.today() is patched to test expiry logic
-**Notification Delivery: External notification senders (email/SMS) are mocked
-**Database Calls: Mocked for isolation from persistence layer

### Test Types
- **Positive Tests**: Valid return dates, valid notifications
- **Negative Tests**: Overdue fines, expired reservations, missing recipients
- **Edge Cases**: Due on same day, leap years, empty messages


### Assertions
- Uses simple assert statements for readability
- Covers return values, state changes, and exceptions
- Clear, readable test assertions
- Comprehensive coverage of return values and side effects

## Test Configuration
[tool:pytest]
testpaths = test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers

```

### Fixtures (conftest.py)
- mock_date: Provides mocked system date
-mock_notification_service: Provides fake notification sender
-setup_environment: Prepares clean environment per test

## Example Test Output

test/test_library_fine_reservation.py::TestFineSystem::test_fine_no_overdue PASSED
test/test_library_fine_reservation.py::TestReservationSystem::test_reservation_expired PASSED
test/test_notification_system.py::TestNotificationSystem::test_send_notification_success PASSED
test/test_notification_system.py::TestNotificationSystem::test_send_notification_missing_user PASSED

======================= 22 passed in 1.45s =======================

```

## Best Practices

1. **Isolation**: Tests independent of database and Flask server
2. **Mocking**: All external dependencies (dates, notifications) are mocked
3. **Clear Naming**: TTest names describe behavior clearly
4. **Comprehensive Coverage**: Covers overdue fines, expiry limits, invalid notifications
5. **Fast Execution**: Runs under 2 seconds

## Continuous Integration

These tests are designed to be easily integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest test/ -v --tb=short


## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure project root in PYTHONPATH
2. **Missing Dependencies**: pytest and pytest-mock
3. **Path Issues**: Use mocked datetime.today()

### Debug Mode
pytest test/ -vv --tb=long   # Verbose with full trace
pytest test/ -v -s           # Show print/log output


