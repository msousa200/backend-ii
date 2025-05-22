"""Custom error classes for the application."""
from typing import Any, Dict, Optional


class AppError(Exception):
    """Base error class for the application"""
    def __init__(self, message: str, error_code: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(AppError):
    """Error raised when input validation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class ProcessingError(AppError):
    """Error raised when text processing fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "PROCESSING_ERROR", details)


class DatabaseError(AppError):
    """Error raised when database operations fail"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "DATABASE_ERROR", details)


class NotFoundError(AppError):
    """Error raised when a requested resource is not found"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "NOT_FOUND", details)


class LanguageDetectionError(AppError):
    """Error raised when language detection fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "LANGUAGE_DETECTION_ERROR", details)


class TranslationError(AppError):
    """Error raised when translation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "TRANSLATION_ERROR", details)


class RateLimitExceededError(AppError):
    """Error raised when rate limit is exceeded"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "RATE_LIMIT_EXCEEDED", details)


def error_to_dict(error: AppError) -> Dict[str, Any]:
    """Convert an AppError to a dictionary for API response"""
    return {
        "error": {
            "code": error.error_code,
            "message": error.message,
            "details": error.details
        }
    }
