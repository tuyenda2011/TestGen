# ===== Tests for normalize_name =====
from source_under_test import normalize_name
import pytest

def test_normalize_name_type_error_TC_009():
    """Ki?m tra normalize_name n�m TypeError khi d?u v�o kh�ng ph?i chu?i."""
    with pytest.raises(TypeError) as exc_info:
        normalize_name(123)
    assert str(exc_info.value) == "name must be a string"

def test_normalize_name_value_error_TC_010():
    """Ki?m tra normalize_name n�m ValueError khi chu?i ch? ch?a kho?ng tr?ng."""
    with pytest.raises(ValueError) as exc_info:
        normalize_name("   ")
    assert str(exc_info.value) == "name cannot be empty"

def test_normalize_name_valid_TC_011():
    """Ki?m tra normalize_name tr? v? chu?i d� trim v� vi?t hoa d?u m?i t?."""
    result = normalize_name("  MyTestName  ")
    assert result == "Mytestname"

# ===== Tests for truncate =====
from source_under_test import truncate

def test_truncate_negative_max_length_TC_012():
    """Ki?m tra truncate n�m ValueError khi max_length �m."""
    with pytest.raises(ValueError) as exc_info:
        truncate("sample", -1)
    assert str(exc_info.value) == "max_length cannot be negative"

def test_truncate_length_equal_TC_013():
    """Ki?m tra truncate tr? v? nguy�n van khi d? d�i b?ng max_length."""
    text = "abcde"
    assert truncate(text, 5) == "abcde"

def test_truncate_max_length_le_3_TC_014():
    """Ki?m tra truncate tr? v? chu?i d?u ch?m khi max_length <= 3."""
    assert truncate("abcdefgh", 3) == "..."
    assert truncate("abcdefgh", 2) == ".."
    assert truncate("abcdefgh", 1) == "."

def test_truncate_typical_case_TC_015():
    """Ki?m tra truncate c?t ng?n v� th�m d?u ba ch?m trong tru?ng h?p th�ng thu?ng."""
    result = truncate("HelloWorld", 8)
    # max_length - 3 = 5, n�n ph?n d?u 5 k� t? + "..."
    assert result == "Hello..."

# ===== Tests for count_ascii_vowels =====
from source_under_test import count_ascii_vowels

def test_count_ascii_vowels_mixed_case_TC_016():
    """Ki?m tra count_ascii_vowels d?m d�ng s? nguy�n �m ASCII trong chu?i h?n h?p."""
    assert count_ascii_vowels("AeIoUxyz") == 5

def test_count_ascii_vowels_no_vowels_TC_017():
    """Ki?m tra count_ascii_vowels tr? v? 0 khi kh�ng c� nguy�n �m."""
    assert count_ascii_vowels("bcdfg") == 0