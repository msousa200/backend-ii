import pytest

def multiply(a, b):
    """
    Multiplies two numbers and returns the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The product of a and b
    """
    return a * b

if __name__ == "__main__":
    print(f"2 * 3 = {multiply(2, 3)}")
    print(f"5 * -2 = {multiply(5, -2)}")
    print(f"0.5 * 4 = {multiply(0.5, 4)}")

def test_multiply():
    """Test the multiply function with various inputs"""
    assert multiply(2, 3) == 6
    
    assert multiply(-1, 4) == -4
    assert multiply(-2, -3) == 6
    
    assert multiply(0, 5) == 0
    
    assert multiply(0.5, 4) == 2.0
    assert multiply(2.5, 2.0) == 5.0

def test_multiply_commutative():
    """Test that multiplication is commutative (a*b = b*a)"""
    a, b = 4, 7
    assert multiply(a, b) == multiply(b, a)

def test_multiply_with_types():
    """Test multiplication with different types"""
    assert multiply(2, 3.0) == 6.0
    
    assert multiply(1000, 1000) == 1000000