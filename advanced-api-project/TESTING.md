# Book API Testing Documentation

## Overview
This document outlines the testing strategy for the Book API endpoints, covering CRUD operations, authentication, permissions, filtering, searching, and ordering functionalities.

## Test Structure
The tests are implemented in `api/test_views.py` using Django's REST Framework test client.

## Test Coverage

### Authentication & Permissions
- **Unauthenticated Access**: Tests that read operations (list, detail) work without authentication
- **Authenticated Operations**: Tests that create, update, delete require authentication
- **Permission Enforcement**: Verifies 401 responses for unauthorized operations

### CRUD Operations
- **Create**: Tests book creation with valid data and authentication
- **Read**: Tests book listing and detail retrieval
- **Update**: Tests book modification with authentication
- **Delete**: Tests book removal with authentication

### Filtering & Search
- **Title Filtering**: Filter books by exact title match
- **Author Filtering**: Filter books by author name using `author__name`
- **Publication Year Filtering**: Filter books by publication year
- **Search Functionality**: Search across title and author name fields

### Ordering
- **Title Ordering**: Sort books alphabetically by title
- **Publication Year Ordering**: Sort books by publication year (ascending/descending)

### Data Validation
- **Future Year Validation**: Prevents books with future publication years
- **Invalid Year Validation**: Prevents books with invalid publication years (< 1000)

## Running Tests

### Method 1: Django Management Command
```bash
python manage.py test api.test_views
```

### Method 2: Specific Test Class
```bash
python manage.py test api.test_views.BookAPITestCase
```

### Method 3: Individual Test Method
```bash
python manage.py test api.test_views.BookAPITestCase.test_book_create_authenticated
```

### Method 4: Using Test Runner Script
```bash
python run_tests.py
```

## Test Data Setup
Each test uses:
- Test user with authentication token
- Test author ("Test Author")
- Two test books with different titles and publication years

## Expected Results
- All tests should pass if the API is functioning correctly
- Failed tests indicate issues with authentication, permissions, or API functionality
- Test output shows detailed information about any failures

## Test Environment
- Uses Django's test database (separate from development/production)
- Automatically creates and destroys test data for each test
- No impact on actual application data

## Interpreting Test Results
- **PASS**: Test executed successfully, functionality works as expected
- **FAIL**: Test failed, indicates a bug or configuration issue
- **ERROR**: Test couldn't run due to setup or code issues

## Adding New Tests
To add new test cases:
1. Add methods to `BookAPITestCase` class
2. Follow naming convention: `test_description_of_what_is_tested`
3. Use appropriate assertions to verify expected behavior
4. Include both positive and negative test scenarios