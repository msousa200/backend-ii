# FastAPI Hello World - Best Practices Example

This project demonstrates a simple "Hello World" FastAPI application that follows web development best practices.

## Key Features

1. **Project Structure**
   - Modular design with clear separation of concerns
   - Environment-based configuration
   - Clean imports and dependencies

2. **Middleware & Request Processing**
   - Request timing middleware
   - CORS configuration
   - Exception handling

3. **Configuration Management**
   - Pydantic settings management
   - Environment variable support
   - Type validation for all settings

4. **Error Handling**
   - Global exception handlers
   - Consistent error response format
   - Proper HTTP status codes

5. **Logging**
   - Structured logging with loggers
   - Request/response logging
   - Different log levels based on environment

6. **API Design**
   - Clean route definitions
   - Path and query parameters
   - Response models and status codes

7. **Testing**
   - Pytest-based unit tests
   - Test client for API testing
   - Fixtures and mocks

## Project Structure

```
fastapi_hello/
├── app/                  # Application package
│   ├── __init__.py
│   ├── config.py         # Configuration management
│   ├── logging_config.py # Logging setup
│   └── main.py           # FastAPI application and routes
├── tests/                # Test directory
│   ├── __init__.py
│   └── test_app.py       # API tests
├── pytest.ini            # Pytest configuration
├── requirements.txt      # Project dependencies
└── run.py                # Application entry point
```

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
   - http://localhost:8000/hello/
   - http://localhost:8000/hello/YourName
   - http://localhost:8000/health/
   - http://localhost:8000/docs (Swagger UI)

## Running Tests

```bash
pytest tests/test_app.py -v
```
