"""
Calculator module with basic arithmetic functions.

This module provides simple arithmetic operations that will be used
to demonstrate CI/CD pipelines with GitHub Actions.
"""

def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b

def divide(a, b):
    """Divide a by b and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    """Return a raised to the power of b."""
    return a ** b

def square(a):
    """Return the square of a number."""
    return a * a

def cube(a):
    """Return the cube of a number."""
    return a * a * a
