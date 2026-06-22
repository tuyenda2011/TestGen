import pytest

# ===== Tests for factorial =====

from source_under_test import factorial

def test_factorial_positive():
    # Ki?m tra nh�nh th�nh c�ng v?i n l� s? nguy�n duong
    assert factorial(5) == 120

def test_factorial_non_integer():
    # Ki?m tra nh�nh th?t b?i khi n kh�ng ph?i l� s? nguy�n
    with pytest.raises(TypeError, match="n must be an integer"):
        factorial('a')

def test_factorial_negative():
    # Ki?m tra nh�nh th?t b?i khi n l� s? �m
    with pytest.raises(ValueError, match="n must be non-negative"):
        factorial(-5)

# ===== Tests for clamp =====

from source_under_test import clamp

def test_clamp_valid_range():
    # Ki?m tra nh�nh th�nh c�ng v?i gi� tr? trong ph?m vi h?p l?
    assert clamp(10, 5, 15) == 10

def test_clamp_invalid_range():
    # Ki?m tra nh�nh th?t b?i khi minimum l?n hon maximum
    with pytest.raises(ValueError, match="minimum cannot be greater than maximum"):
        clamp(10, 15, 5)

def test_clamp_below_minimum():
    # Ki?m tra nh�nh th�nh c�ng v?i gi� tr? nh? hon minimum
    assert clamp(5, 10, 15) == 10

def test_clamp_above_maximum():
    # Ki?m tra nh�nh th�nh c�ng v?i gi� tr? l?n hon maximum
    assert clamp(20, 5, 15) == 15

# ===== Tests for safe_divide =====

from source_under_test import safe_divide

def test_safe_divide_valid_input():
    # Ki?m tra nh�nh th�nh c�ng v?i t? s? v� m?u d?u l� s? th?c
    assert safe_divide(10, 2) == 5.0

def test_safe_divide_zero_denominator():
    # Ki?m tra nh�nh th?t b?i khi m?u b?ng 0
    with pytest.raises(ZeroDivisionError, match="denominator cannot be zero"):
        safe_divide(10, 0)