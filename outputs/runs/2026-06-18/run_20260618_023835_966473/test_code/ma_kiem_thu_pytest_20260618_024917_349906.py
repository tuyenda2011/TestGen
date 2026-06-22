# ===== Tests for factorial =====
from source_under_test import factorial
import pytest

def test_factorial_valid_input():
    """Ki?m tra t�nh giai th?a v?i d?u v�o h?p l?."""
    assert factorial(5) == 120
    assert factorial(0) == 1

def test_factorial_type_error():
    """Ki?m tra r?ng TypeError du?c n�m khi n kh�ng ph?i int."""
    with pytest.raises(TypeError) as excinfo:
        factorial(3.5)
    assert str(excinfo.value) == "n must be an integer"

def test_factorial_negative_value():
    """Ki?m tra r?ng ValueError du?c n�m khi n �m."""
    with pytest.raises(ValueError) as excinfo:
        factorial(-2)
    assert str(excinfo.value) == "n must be non-negative"

# ===== Tests for clamp =====
from source_under_test import clamp

def test_clamp_normal_range():
    """Ki?m tra gi� tr? n?m trong kho?ng tr? v? nguy�n gi� tr?."""
    assert clamp(5.0, 1.0, 10.0) == 5.0

def test_clamp_below_minimum():
    """Ki?m tra gi� tr? nh? hon minimum tr? v? minimum."""
    assert clamp(-2.0, 0.0, 5.0) == 0.0

def test_clamp_above_maximum():
    """Ki?m tra gi� tr? l?n hon maximum tr? v? maximum."""
    assert clamp(12.0, 0.0, 10.0) == 10.0

def test_clamp_invalid_bounds():
    """Ki?m tra r?ng ValueError du?c n�m khi minimum > maximum."""
    with pytest.raises(ValueError) as excinfo:
        clamp(3.0, 5.0, 2.0)
    assert str(excinfo.value) == "minimum cannot be greater than maximum"

# ===== Tests for safe_divide =====
from source_under_test import safe_divide

def test_safe_divide_normal():
    """Ki?m tra ph�p chia b�nh thu?ng tr? v? k?t qu? d�ng."""
    assert safe_divide(10.0, 2.0) == 5.0

def test_safe_divide_zero_denominator():
    """Ki?m tra r?ng ZeroDivisionError du?c n�m khi m?u s? b?ng 0."""
    with pytest.raises(ZeroDivisionError) as excinfo:
        safe_divide(5.0, 0.0)
    assert str(excinfo.value) == "denominator cannot be zero"