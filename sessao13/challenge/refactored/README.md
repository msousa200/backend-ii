# Web Application Refactoring - Best Practices Challenge

This project demonstrates the refactoring of a poorly structured web application into one that follows best practices for web development.

## Before and After

### Before (`before_refactor.py`)
The original application has several issues:
- Poor database connection management
- No structured error handling
- Missing input validation
- No proper logging
- Mixed concerns without separation
- Synchronous operations blocking the event loop
- No tests or documentation

### After (`refactored/`)
The refactored application implements:
- Clear project structure with separation of concerns
- Asynchronous database operations
- Connection pooling with proper resource management
- Middleware for security and performance
- Comprehensive error handling
- Input validation with Pydantic models
- Performance measurement with decorators
- Structured logging
- Unit tests

## Project Structure

```
refactored/
├── app/                      # Main application package
│   ├── __init__.py
│   ├── main.py               # FastAPI application setup
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   └── routes.py         # Route definitions
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py         # Application configuration
│   │   └── logging_config.py # Logging setup
│   ├── db/                   # Database layer
│   │   ├── __init__.py
│   │   └── database.py       # Database connections and operations
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   └── product.py        # Product models
│   └── utils/                # Utility functions
│       ├── __init__.py
│       └── performance.py    # Performance measurement tools
├── tests/                    # Test directory
│   ├── __init__.py
│   └── test_api.py           # API tests
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Project dependencies
└── run.py                    # Application entry point
```

## Key Improvements

### 1. Asynchronous Programming
- Replaced synchronous SQLite with asynchronous aiosqlite
- Properly managed connection pools and resources
- Implemented async endpoints and database operations

### 2. Error Handling
- Global exception handlers for consistent responses
- Proper error logging and tracing
- Type-specific exception handling

### 3. Validation
- Pydantic models for request/response validation
- Data validation at multiple levels (API, database)
- Clear validation error messages

### 4. Performance Monitoring
- Request timing middleware
- Performance measurement decorators
- Database operation timing

### 5. Security
- CORS configuration
- Trusted hosts middleware
- Input sanitization

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the application:
   ```bash
   python run.py
   ```

3. Access the API at:
   - http://localhost:8000/products/
   - http://localhost:8000/products/{id}
   - http://localhost:8000/docs (Swagger UI)

## Running Tests

```bash
pytest tests/test_api.py -v
```
