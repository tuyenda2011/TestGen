# ===== Tests for normalize_name =====
from source_under_test import normalize_name

def test_normalize_name_valid_input():
    # Ki?m tra ch?c nang chu?n h�a t�n v?i chu?i d?u v�o h?p l? c� kho?ng tr?ng.
    assert normalize_name('  ExampleName  ') == 'Examplename'

def test_normalize_name_non_string_input():
    # Ki?m tra vi?c n�m TypeError khi d?u v�o kh�ng ph?i l� chu?i.
    import pytest
    with pytest.raises(TypeError, match="name must be a string"):
        normalize_name(12345)

def test_normalize_name_empty_after_cleaning():
    # Ki?m tra vi?c n�m ValueError khi chu?i tr?ng sau khi x? l�.
    import pytest
    with pytest.raises(ValueError, match="name cannot be empty"):
        normalize_name('   ')

def test_normalize_name_single_character():
    # Ki?m tra x? l� d�ng v?i chu?i m?t k� t?.
    assert normalize_name(' A ') == 'A'

# ===== Tests for truncate =====
from source_under_test import truncate

def test_truncate_text_shorter_than_max_length():
    # Ki?m tra tr? v? van b?n g?c khi d? d�i nh? hon ho?c b?ng max_length.
    assert truncate('Hello', 10) == 'Hello'

def test_truncate_text_longer_with_ellipsis():
    # Ki?m tra c?t ng?n van b?n v� th�m d?u ba ch?m khi max_length > 3.
    assert truncate('HelloWorld', 5) == 'He...'

def test_truncate_max_length_less_than_or_equal_three():
    # Ki?m tra tr? v? c�c d?u ch?m khi max_length <= 3.
    assert truncate('Testing', 3) == '...'

def test_truncate_negative_max_length():
    # Ki?m tra vi?c n�m ValueError khi max_length l� s? �m.
    import pytest
    with pytest.raises(ValueError, match="max_length cannot be negative"):
        truncate('Any', -1)

# ===== Tests for count_ascii_vowels =====
from source_under_test import count_ascii_vowels

def test_count_ascii_vowels_mixed_case():
    # Ki?m tra d?m d�ng s? nguy�n �m trong chu?i c� ch? hoa/thu?ng.
    assert count_ascii_vowels('AeIoUxyz') == 5

def test_count_ascii_vowels_no_vowels():
    # Ki?m tra tr? v? 0 khi kh�ng c� nguy�n �m n�o trong chu?i.
    assert count_ascii_vowels('bcdfg') == 0

def test_count_ascii_vowels_empty_string():
    # Ki?m tra tr? v? 0 v?i chu?i r?ng.
    assert count_ascii_vowels('') == 0