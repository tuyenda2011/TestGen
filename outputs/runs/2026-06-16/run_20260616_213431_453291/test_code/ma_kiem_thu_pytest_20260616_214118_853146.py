# ===== Tests for normalize_name =====
from source_under_test import normalize_name

def test_normalize_name_valid_input():
    # Ki?m tra ch?c nang chu?n h�a t�n: c?t kho?ng tr?ng v� vi?t hoa ch? c�i d?u m?i t?.
    assert normalize_name("  Alice Smith  ") == "Alice Smith"

def test_normalize_name_non_string_raises_typeerror():
    # Ki?m tra ngo?i l? TypeError khi d?u v�o kh�ng ph?i l� chu?i.
    import pytest
    with pytest.raises(TypeError, match="name must be a string"):
        normalize_name(12345)

def test_normalize_name_empty_after_cleaning_raises_valueerror():
    # Ki?m tra ngo?i l? ValueError khi chu?i ch? ch?a kho?ng tr?ng.
    import pytest
    with pytest.raises(ValueError, match="name cannot be empty"):
        normalize_name("   ")

# ===== Tests for truncate =====
from source_under_test import truncate

def test_truncate_within_limit():
    # Ki?m tra tr? v? nguy�n van khi d? d�i van b?n nh? hon ho?c b?ng max_length.
    assert truncate("hello", 10) == "hello"

def test_truncate_max_length_three_or_less():
    # Ki?m tra tr? v? d?u ch?m (...) khi max_length nh? hon ho?c b?ng 3.
    assert truncate("abcdef", 3) == "..."

def test_truncate_negative_max_length_raises_valueerror():
    # Ki?m tra ngo?i l? ValueError khi max_length l� s? �m.
    import pytest
    with pytest.raises(ValueError, match="max_length cannot be negative"):
        truncate("test", -1)

def test_truncate_exceeds_limit():
    # Ki?m tra c?t van b?n v� th�m d?u ba ch?m khi vu?t qu� max_length.
    assert truncate("hello world", 8) == "hello..."

# ===== Tests for count_ascii_vowels =====
from source_under_test import count_ascii_vowels

def test_count_ascii_vowels_mixed_characters():
    # Ki?m tra d?m nguy�n �m ti?ng Anh trong chu?i c� ch? c�i, s? v� k� t? d?c bi?t.
    assert count_ascii_vowels("Hello, World! 123") == 3

def test_count_ascii_vowels_empty_string():
    # Ki?m tra tr? v? 0 khi chu?i r?ng.
    assert count_ascii_vowels("") == 0

def test_count_ascii_vowels_all_vowels():
    # Ki?m tra d?m d�ng t?t c? c�c nguy�n �m trong chu?i ch? g?m nguy�n �m.
    assert count_ascii_vowels("aeiouAEIOU") == 10

def test_count_ascii_vowels_no_vowels():
    # Ki?m tra tr? v? 0 khi chu?i kh�ng ch?a nguy�n �m.
    assert count_ascii_vowels("xyz123!@#") == 0