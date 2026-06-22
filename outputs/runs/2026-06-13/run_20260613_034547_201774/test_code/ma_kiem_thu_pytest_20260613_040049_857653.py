from inline_snapshot import snapshot

import pytest

# ===== Tests for normalize_name =====
from source_under_test import normalize_name

def test_normalize_name_tra_ve_chuoi_da_chuan_hoa_khi_dau_vao_hop_le():
    assert normalize_name('  John   Doe  ') == snapshot('John Doe')

def test_normalize_name_nem_TypeError_khi_dau_vao_khong_phai_chuoi():
    with pytest.raises(TypeError, match="name must be a string"):
        normalize_name(12345)

def test_normalize_name_nem_ValueError_khi_chuoi_chi_chua_khoang_trang():
    with pytest.raises(ValueError, match="name cannot be empty"):
        normalize_name('   ')

def test_normalize_name_nem_ValueError_khi_chuoi_rong():
    with pytest.raises(ValueError, match="name cannot be empty"):
        normalize_name('')

# ===== Tests for truncate =====
from source_under_test import truncate

def test_truncate_tra_ve_chuoi_nguyen_ban_khi_do_dai_nho_hon_max_length():
    assert truncate('Hello', 10) == snapshot('Hello')

def test_truncate_cat_ngan_chuoi_dung_khi_max_length_lon_hon_3_va_nho_hon_chieu_dai_text():
    assert truncate('HelloWorld', 5) == snapshot('He...')

def test_truncate_tra_ve_chuoi_goc_khi_max_length_nho_hon_hoac_bang_3():
    assert truncate('Hello', 3) == snapshot('...')

def test_truncate_tra_ve_cham_khi_max_length_bang_1():
    assert truncate('Hello', 1) == snapshot('.')

def test_truncate_tra_ve_cham_khi_max_length_bang_2():
    assert truncate('Hello', 2) == snapshot('..')

def test_truncate_nem_ValueError_khi_max_length_am():
    with pytest.raises(ValueError, match="max_length cannot be negative"):
        truncate('Test', -1)

def test_truncate_tra_ve_chuoi_goc_khi_chieu_dai_bang_max_length():
    assert truncate('Hello', 5) == snapshot('Hello')

# ===== Tests for count_ascii_vowels =====
from source_under_test import count_ascii_vowels

def test_count_ascii_vowels_tra_ve_so_nguyen_am_trong_chuoi_ascii():
    assert count_ascii_vowels('Education') == snapshot(5)

def test_count_ascii_vowels_tra_ve_0_khi_khong_co_nguyen_am():
    assert count_ascii_vowels('bcdfg') == snapshot(0)

def test_count_ascii_vowels_kiem_tra_chu_hoa():
    assert count_ascii_vowels('AEIOU') == snapshot(5)

def test_count_ascii_vowels_kiem_tra_chu_thuong():
    assert count_ascii_vowels('aeiou') == snapshot(5)

def test_count_ascii_vowels_kiem_tra_phu_ap_pha():
    assert count_ascii_vowels('Programming') == snapshot(3)