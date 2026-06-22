# ===== Tests for factorial =====
from source_under_test import factorial
import pytest

def test_factorial_positive():
    """Ki?m tra t�nh giai th?a c?a s? nguy�n duong."""
    assert factorial(5) == 120
    assert factorial(0) == 1

def test_factorial_type_error():
    """Ki?m tra vi?c raise TypeError khi d?u v�o kh�ng ph?i int."""
    with pytest.raises(TypeError) as exc:
        factorial(3.5)
    assert str(exc.value) == "n must be an integer"

def test_factorial_value_error():
    """Ki?m tra vi?c raise ValueError khi n �m."""
    with pytest.raises(ValueError) as exc:
        factorial(-2)
    assert str(exc.value) == "n must be non-negative"

# ===== Tests for clamp =====
from source_under_test import clamp

def test_clamp_within_range():
    """Gi� tr? n?m trong kho?ng tr? v? nguy�n gi� tr?."""
    assert clamp(5.0, 1.0, 10.0) == 5.0

def test_clamp_below_minimum():
    """Gi� tr? nh? hon minimum tr? v? minimum."""
    assert clamp(-2.0, 0.0, 3.0) == 0.0

def test_clamp_above_maximum():
    """Gi� tr? l?n hon maximum tr? v? maximum."""
    assert clamp(8.0, 0.0, 5.0) == 5.0

def test_clamp_invalid_range():
    """Ki?m tra raise ValueError khi minimum l?n hon maximum."""
    with pytest.raises(ValueError) as exc:
        clamp(1.0, 10.0, 5.0)
    assert str(exc.value) == "minimum cannot be greater than maximum"

# ===== Tests for safe_divide =====
from source_under_test import safe_divide

def test_safe_divide_normal():
    """Ki?m tra ph�p chia b�nh thu?ng."""
    assert safe_divide(10.0, 2.0) == 5.0

def test_safe_divide_zero_denominator():
    """Ki?m tra raise ZeroDivisionError khi m?u s? b?ng 0."""
    with pytest.raises(ZeroDivisionError) as exc:
        safe_divide(1.0, 0.0)
    assert str(exc.value) == "denominator cannot be zero"