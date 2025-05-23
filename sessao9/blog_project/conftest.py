"""
Configuration for pytest
"""
import pytest
from django.conf import settings

def pytest_configure():
    """Configure Django settings for tests"""
    settings.DEBUG = False
    settings.PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
    settings.SECRET_KEY = 'test-key-for-testing-purposes-only'
