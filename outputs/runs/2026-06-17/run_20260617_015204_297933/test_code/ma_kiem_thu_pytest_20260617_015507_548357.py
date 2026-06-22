# ===== Tests for normalize_name =====
from source_under_test import normalize_name
import pytest

def test_normalize_name_valid_input():
    """Ki?m tra h�m tr? v? t�n d� chu?n ho� khi d?u v�o h?p l?."""
    assert normalize_name("  ExampleName  ") == "Examplename"

def test_normalize_name_type_error():
    """Ki?m tra h�m n�m TypeError khi d?u v�o kh�ng ph?i chu?i."""
    with pytest.raises(TypeError) as exc:
        normalize_name(12345)
    assert str(exc.value) == "name must be a string"

def test_normalize_name_value_error_empty():
    """Ki?m tra h�m n�m ValueError khi chu?i sau khi l�m s?ch r?ng."""
    with pytest.raises(ValueError) as exc:
        normalize_name("   ")
    assert str(exc.value) == "name cannot be empty"

# ===== Tests for truncate =====
from source_under_test import truncate

def test_truncate_original_when_shorter():
    """Ki?m tra tr? v? nguy�n van khi d? d�i <= max_length."""
    assert truncate("hello", 10) == "hello"

def test_truncate_negative_max_length():
    """Ki?m tra n�m ValueError khi max_length �m."""
    with pytest.raises(ValueError) as exc:
        truncate("test", -5)
    assert str(exc.value) == "max_length cannot be negative"

def test_truncate_ellipsis_when_max_le_3():
    """Ki?m tra tr? v? d?u ch?m khi max_length <= 3."""
    assert truncate("abcdef", 3) == "..."
    assert truncate("abcdef", 2) == ".."
    assert truncate("abcdef", 1) == "."

def test_truncate_truncates_and_adds_ellipsis():
    """Ki?m tra c?t chu?i v� th�m '...' khi c?n thi?t."""
    assert truncate("abcdefghij", 7) == "abcd..."
    # max_length 4 -> one char + '...'
    assert truncate("12345", 4) == "1..."

# ===== Tests for count_ascii_vowels =====
from source_under_test import count_ascii_vowels

def test_count_ascii_vowels_mixed_case():
    """Ki?m tra d?m nguy�n �m trong chu?i c� c? ch? hoa v� thu?ng."""
    assert count_ascii_vowels("AeIoUxyz") == 5

def test_count_ascii_vowels_no_vowels():
    """Ki?m tra tr? v? 0 khi chu?i kh�ng ch?a nguy�n �m."""
    assert count_ascii_vowels("bcdfg") == 0

def test_count_ascii_vowels_empty_string():
    """Ki?m tra tr? v? 0 cho chu?i r?ng."""
    assert count_ascii_vowels("") == 0