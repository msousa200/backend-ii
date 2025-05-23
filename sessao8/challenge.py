import pytest

def factorial(n):
    """
    Calculate the factorial of a number recursively.
    
    Args:
        n: A non-negative integer
        
    Returns:
        The factorial of n (n!)
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    if not isinstance(n, int):
        raise TypeError("Factorial is only defined for integers")
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    if n == 0 or n == 1:
        return 1
    
    return n * factorial(n - 1)

if __name__ == "__main__":
    try:
        num = int(input("Enter a non-negative integer: "))
        result = factorial(num)
        print(f"The factorial of {num} is {result}")
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")

def test_factorial_basic():
    """Basic test for factorial function"""
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120

@pytest.mark.parametrize("n,expected", [
    (0, 1),            
    (1, 1),            
    (2, 2),            
    (3, 6),           
    (4, 24),           
    (5, 120),        
    (10, 3628800),    
])
def test_factorial_parametrized(n, expected):
    """Test factorial function with parametrized inputs"""
    assert factorial(n) == expected

def test_factorial_negative():
    """Test that factorial raises ValueError for negative inputs"""
    with pytest.raises(ValueError):
        factorial(-1)
    
    with pytest.raises(ValueError):
        factorial(-5)

def test_factorial_non_integer():
    """Test that factorial raises TypeError for non-integer inputs"""
    with pytest.raises(TypeError):
        factorial(3.5)
    
    with pytest.raises(TypeError):
        factorial("5")

def test_factorial_large_input():
    """Test factorial with a larger input"""
    assert factorial(20) == 2432902008176640000