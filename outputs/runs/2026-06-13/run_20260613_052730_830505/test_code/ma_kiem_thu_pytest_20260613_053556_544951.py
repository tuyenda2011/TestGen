from inline_snapshot import snapshot

import pytest

# ===== Tests for normalize_name =====
from source_under_test import normalize_name

def test_normalize_name_valid_input():
    # Kiểm tra chuỗi hợp lệ trả về tên đã chuẩn hóa
    assert normalize_name('  Nguyen Van A  ') == snapshot('Nguyen Van A')

def test_normalize_name_non_string_input():
    # Kiểm tra đầu vào không phải chuỗi ném TypeError
    with pytest.raises(TypeError, match="name must be a string"):
        normalize_name(123)

def test_normalize_name_empty_string():
    # Kiểm tra chuỗi rỗng ném ValueError
    with pytest.raises(ValueError, match="name cannot be empty"):
        normalize_name('')

def test_normalize_name_whitespace_only():
    # Kiểm tra chuỗi chỉ chứa khoảng trắng ném ValueError
    with pytest.raises(ValueError, match="name cannot be empty"):
        normalize_name('   ')

def test_normalize_name_single_word():
    # Kiểm tra chuỗi một từ đơn giản
    assert normalize_name('hello') == snapshot('Hello')

def test_normalize_name_multiple_spaces():
    # Kiểm tra chuỗi có nhiều khoảng trắng liên tiếp được chuẩn hóa
    assert normalize_name('John   Doe') == snapshot('John Doe')

# ===== Tests for truncate =====
from source_under_test import truncate

def test_truncate_text_shorter_than_max_length():
    # Kiểm tra văn bản ngắn hơn max_length trả về nguyên văn
    assert truncate('Hello', 10) == snapshot('Hello')

def test_truncate_text_longer_than_max_length():
    # Kiểm tra văn bản dài hơn max_length bị cắt ngắn
    assert truncate('Hello World', 8) == snapshot('Hello...')

def test_truncate_negative_max_length():
    # Kiểm tra max_length âm ném ValueError
    with pytest.raises(ValueError, match="max_length cannot be negative"):
        truncate('Hello', -1)

def test_truncate_max_length_equals_three():
    # Kiểm tra max_length = 3 trả về dấu chấm
    assert truncate('Hello', 3) == snapshot('...')

def test_truncate_max_length_less_than_three():
    # Kiểm tra max_length < 3 trả về chuỗi dấu chấm
    assert truncate('Hello', 2) == snapshot('..')

def test_truncate_max_length_equals_text_length():
    # Kiểm tra max_length bằng độ dài văn bản
    assert truncate('Hello', 5) == snapshot('Hello')

def test_truncate_max_length_greater_than_text_length():
    # Kiểm tra max_length lớn hơn độ dài văn bản
    assert truncate('Hi', 10) == snapshot('Hi')

def test_truncate_max_length_four():
    # Kiểm tra max_length = 4 trả về chuỗi cắt có ellipsis
    assert truncate('Hello World', 4) == snapshot('H...')

# ===== Tests for count_ascii_vowels =====
from source_under_test import count_ascii_vowels

def test_count_ascii_vowels_mixed_case():
    # Kiểm tra chuỗi chứa nguyên âm in hoa và thường
    assert count_ascii_vowels('Hello World') == snapshot(3)

def test_count_ascii_vowels_empty_string():
    # Kiểm tra chuỗi rỗng trả về 0
    assert count_ascii_vowels('') == snapshot(0)

def test_count_ascii_vowels_no_vowels():
    # Kiểm tra chuỗi không chứa nguyên âm ASCII
    assert count_ascii_vowels('bcdfg') == snapshot(0)

def test_count_ascii_vowels_all_vowels():
    # Kiểm tra chuỗi chỉ chứa nguyên âm
    assert count_ascii_vowels('aeiouAEIOU') == snapshot(10)

def test_count_ascii_vowels_all_uppercase():
    # Kiểm tra chuỗi chỉ chứa nguyên âm in hoa
    assert count_ascii_vowels('AEIOU') == snapshot(5)

def test_count_ascii_vowels_all_lowercase():
    # Kiểm tra chuỗi chỉ chứa nguyên âm in thường
    assert count_ascii_vowels('aeiou') == snapshot(5)

def test_count_ascii_vowels_with_numbers():
    # Kiểm tra chuỗi chứa số và nguyên âm
    assert count_ascii_vowels('h3ll0 w0rld') == snapshot(0)

def test_count_ascii_vowels_special_chars():
    # Kiểm tra chuỗi chứa ký tự đặc biệt
    assert count_ascii_vowels('!@#$%a^e&*i(o)u') == snapshot(5)