# ===== Tests for factorial =====
from source_under_test import factorial
import pytest

def test_factorial_typical_input_TC_011():
    """Ki?m tra factorial tr? v? 120 khi n=5."""
    assert factorial(5) == 120

def test_factorial_zero_TC_014():
    """Ki?m tra factorial tr? v? 1 khi n=0."""
    assert factorial(0) == 1

def test_factorial_type_error_TC_012():
    """Ki?m tra factorial n kh�ng ph?i int g�y TypeError."""
    with pytest.raises(TypeError) as exc:
        factorial('5')
    assert str(exc.value) == "n must be an integer"

def test_factorial_negative_value_TC_013():
    """Ki?m tra factorial n �m g�y ValueError."""
    with pytest.raises(ValueError) as exc:
        factorial(-3)
    assert str(exc.value) == "n must be non-negative"

# ===== Tests for clamp =====
from source_under_test import clamp

def test_clamp_within_range_TC_015():
    """Ki?m tra clamp tr? v? gi� tr? kh�ng thay d?i khi n?m trong kho?ng."""
    assert clamp(5, 1, 10) == 5

def test_clamp_minimum_greater_than_maximum_TC_016():
    """Ki?m tra clamp khi minimum > maximum g�y ValueError."""
    with pytest.raises(ValueError) as exc:
        clamp(5, 10, 1)
    assert str(exc.value) == "minimum cannot be greater than maximum"

def test_clamp_below_minimum_TC_017():
    """Ki?m tra clamp tr? v? minimum khi gi� tr? du?i minimum."""
    assert clamp(-2, 0, 10) == 0

def test_clamp_above_maximum_TC_018():
    """Ki?m tra clamp tr? v? maximum khi gi� tr? tr�n maximum."""
    assert clamp(15, 0, 10) == 10

# ===== Tests for safe_divide =====
from source_under_test import safe_divide

def test_safe_divide_normal_TC_019():
    """Ki?m tra safe_divide tr? v? thuong khi m?u s? kh�c 0."""
    assert safe_divide(10, 2) == 5.0

def test_safe_divide_zero_denominator_TC_020():
    """Ki?m tra safe_divide v?i m?u s? 0 g�y ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError) as exc:
        safe_divide(10, 0)
    assert str(exc.value) == "denominator cannot be zero"