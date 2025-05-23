# Django Hello World - Best Practices Example

This project demonstrates a simple "Hello World" Django application that follows web development best practices.

## Key Features

1. **Project Structure**
   - Proper separation between project settings and application code
   - Well-organized settings with clear sections
   - Modular URL configurations

2. **Middleware & Request Processing**
   - Custom middleware for request logging
   - Request timing measurements
   - Performance monitoring

3. **Error Handling**
   - Custom exception middleware
   - Structured error responses
   - Proper HTTP status codes

4. **Logging**
   - Comprehensive logging configuration
   - Different log levels for development and production
   - Request/response logging

5. **Security**
   - Basic security headers
   - CORS configuration
   - Protection against common vulnerabilities

6. **API Design**
   - RESTful API endpoints
   - Django REST Framework integration
   - Proper content negotiation

7. **Testing**
   - Unit tests for views and models
   - Test isolation best practices
   - Pytest integration

## Project Structure

```
django_hello/
├── hello_app/            # Main application code
│   ├── __init__.py
│   ├── apps.py           # App configuration
│   ├── tests.py          # Unit tests
│   ├── urls.py           # URL routing
│   └── views.py          # View functions
├── hello_project/        # Django project settings
│   ├── __init__.py
│   ├── asgi.py           # ASGI config
│   ├── middleware.py     # Custom middleware
│   ├── settings.py       # Project settings
│   ├── urls.py           # Root URL config
│   └── wsgi.py           # WSGI config
├── manage.py             # Django command-line tool
├── pytest.ini            # Pytest configuration
└── requirements.txt      # Project dependencies
```

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Apply migrations:
   ```bash
   python manage.py migrate
   ```

3. Start the development server:
   ```bash
   python manage.py runserver
   ```

4. Access the API at:
   - http://localhost:8000/api/hello/
   - http://localhost:8000/api/hello/?name=YourName

## Running Tests

```bash
python manage.py test
```

Or with pytest:

```bash
pytest
```
