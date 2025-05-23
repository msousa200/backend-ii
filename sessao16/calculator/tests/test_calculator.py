"""
Unit tests for the calculator module.

These tests verify that our calculator functions work correctly.
"""

import pytest
from calculator import add, subtract, multiply, divide, power, square, cube


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(2, 4) == -2
    assert subtract(0, 0) == 0


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(5, 0) == 0
    assert multiply(-2, -3) == 6


def test_divide():
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    assert divide(-6, 2) == -3


    with pytest.raises(ValueError):
        divide(5, 0)


def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1
    assert power(2, -1) == 0.5


def test_square():
    assert square(2) == 4
    assert square(0) == 0
    assert square(-3) == 9


def test_cube():
    assert cube(2) == 8
    assert cube(0) == 0
    assert cube(-3) == -27
