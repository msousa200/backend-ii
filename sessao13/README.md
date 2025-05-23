# Session 13: Web Development Best Practices with Django and FastAPI

This session focuses on proper code organization, error handling, security, and performance optimization in Django and FastAPI web frameworks.

## Exercise: Hello World Applications with Best Practices

Two minimal "Hello World" applications demonstrating proper project structure and best practices:

### Django Project (`django_hello/`)

A Django application demonstrating:

- Proper project structure
- Custom middleware for request logging
- Comprehensive logging configuration
- Error handling with appropriate HTTP responses
- REST API endpoint using Django REST Framework

#### Running the Django application:

```bash
cd django_hello
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit: http://localhost:8000/api/hello/

### FastAPI Project (`fastapi_hello/`)

A FastAPI application demonstrating:

- Clean modular project organization
- Middleware for request timing and CORS
- Pydantic settings management
- Proper error handling with status codes
- Input validation
- Comprehensive logging

#### Running the FastAPI application:

```bash
cd fastapi_hello
pip install -r requirements.txt
python run.py
```

Visit: http://localhost:8000/hello/ or http://localhost:8000/docs

## Challenge: Refactoring for Best Practices

The challenge demonstrates refactoring a poorly structured web application into one that follows best practices.

### Before Refactoring (`challenge/before_refactor.py`)

A simple FastAPI application with several problems:

- Poor connection management
- No structured error handling
- Missing input validation
- No proper logging
- Mixed concerns without separation
- Synchronous operations blocking the event loop

### After Refactoring (`challenge/refactored/`)

The refactored application implements:

- Clear project structure with separation of concerns
- Asynchronous database operations
- Connection pooling
- Middleware for security (CORS, trusted hosts)
- Comprehensive error handling
- Input validation with Pydantic
- Performance measurement with decorators
- Structured logging

#### Running the refactored application:

```bash
cd challenge/refactored
pip install -r requirements.txt
python run.py
```

Visit: http://localhost:8000/products/ or http://localhost:8000/docs

## Running Tests

### Django Project Tests
```bash
cd django_hello
pip install pytest pytest-django
python manage.py test
```

### FastAPI Project Tests
```bash
cd fastapi_hello
pip install pytest httpx
pytest tests/test_app.py -v
```

### Refactored Challenge Tests
```bash
cd challenge/refactored
pip install pytest httpx
pytest tests/test_api.py -v
```

## Docker Support

All three projects include Docker configuration for containerized deployment, which is another best practice for modern web applications.

### Running with Docker

Individual containers:
```bash
# Django app
cd django_hello
docker build -t django-hello .
docker run -p 8001:8000 django-hello

# FastAPI app
cd fastapi_hello
docker build -t fastapi-hello .
docker run -p 8002:8000 fastapi-hello

# Challenge app
cd challenge/refactored
docker build -t challenge-app .
docker run -p 8003:8000 challenge-app
```

### Running with Docker Compose

To run all three applications at once:
```bash
docker-compose up -d
```

Access the applications at:
- Django: http://localhost:8001/api/hello/
- FastAPI: http://localhost:8002/hello/
- Challenge: http://localhost:8003/products/

## Key Best Practices Demonstrated

1. **Project Structure**
   - Separation of concerns
   - Modular organization
   - Config management

2. **Error Handling**
   - Custom exception handlers
   - Proper HTTP status codes
   - Meaningful error messages

3. **Security**
   - CORS configuration
   - Trusted hosts validation
   - Input validation

4. **Performance**
   - Asynchronous operations
   - Connection pooling
   - Middleware for monitoring

5. **Logging**
   - Structured logging
   - Different log levels
   - Custom formatting

6. **Testing**
   - Unit tests with pytest for FastAPI
   - Unit tests with Django's test framework
   - Test fixtures and mocks
   - Database testing isolation
