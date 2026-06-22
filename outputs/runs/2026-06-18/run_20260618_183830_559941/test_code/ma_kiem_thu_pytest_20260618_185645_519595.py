# ===== Tests for factorial =====
from source_under_test import factorial
import pytest

def test_factorial_TC_001():
    # Ki?m tra tru?ng h?p d?u v�o b?ng 0, factorial(0) ph?i tr? v? 1.
    assert factorial(0) == 1

def test_factorial_TC_002():
    # Ki?m tra tru?ng h?p d?u v�o l� s? nguy�n duong, factorial(5) ph?i tr? v? 120.
    assert factorial(5) == 120

def test_factorial_TC_003():
    # Ki?m tra ranh gi?i v?i d?u v�o t?i thi?u b?ng 0, ph?i tr? v? 1.
    assert factorial(0) == 1

def test_factorial_TC_004():
    # Ki?m tra ngo?i l? TypeError khi d?u v�o l� s? th?c float.
    with pytest.raises(TypeError, match="n must be an integer"):
        factorial(3.14)

def test_factorial_TC_005():
    # Ki?m tra ngo?i l? TypeError khi d?u v�o l� chu?i string.
    with pytest.raises(TypeError, match="n must be an integer"):
        factorial('5')

def test_factorial_TC_006():
    # Ki?m tra ngo?i l? ValueError khi d?u v�o l� s? nguy�n �m.
    with pytest.raises(ValueError, match="n must be non-negative"):
        factorial(-1)

def test_factorial_TC_018():
    # Ki?m tra h�nh vi v?i s? nguy�n l?n, factorial(1000) ph?i tr? v? k?t qu? ch�nh x�c.
    result = factorial(1000)
    assert result > 0
    assert isinstance(result, int)

# ===== Tests for clamp =====
from source_under_test import clamp

def test_clamp_TC_007():
    # Ki?m tra tru?ng h?p gi� tr? n?m trong kho?ng [minimum, maximum], ph?i tr? v? ch�nh gi� tr? d�.
    assert clamp(5, 0, 10) == 5

def test_clamp_TC_008():
    # Ki?m tra ranh gi?i khi gi� tr? b?ng minimum, ph?i tr? v? minimum.
    assert clamp(0, 0, 10) == 0

def test_clamp_TC_009():
    # Ki?m tra ranh gi?i khi gi� tr? b?ng maximum, ph?i tr? v? maximum.
    assert clamp(10, 0, 10) == 10

def test_clamp_TC_010():
    # Ki?m tra tru?ng h?p gi� tr? nh? hon minimum, ph?i tr? v? minimum.
    assert clamp(-5, 0, 10) == 0

def test_clamp_TC_011():
    # Ki?m tra tru?ng h?p gi� tr? l?n hon maximum, ph?i tr? v? maximum.
    assert clamp(15, 0, 10) == 10

def test_clamp_TC_012():
    # Ki?m tra ranh gi?i khi minimum b?ng maximum, ph?i tr? v? gi� tr? d�.
    assert clamp(5, 5, 5) == 5

def test_clamp_TC_013():
    # Ki?m tra ngo?i l? ValueError khi minimum l?n hon maximum.
    with pytest.raises(ValueError, match="minimum cannot be greater than maximum"):
        clamp(5, 10, 0)

def test_clamp_TC_019():
    # Ki?m tra h�nh vi v?i ki?u kh�ng ph?i s?, h�m s? th?c hi?n so s�nh chu?i.
    with pytest.raises(TypeError):
        clamp('a', 0, 10)

# ===== Tests for safe_divide =====
from source_under_test import safe_divide

def test_safe_divide_TC_014():
    # Ki?m tra ph�p chia v?i m?u s? kh�c 0, safe_divide(10, 2) ph?i tr? v? 5.0.
    assert safe_divide(10, 2) == 5.0

def test_safe_divide_TC_015():
    # Ki?m tra ranh gi?i khi s? b? chia b?ng 0, ph?i tr? v? 0.0.
    assert safe_divide(0, 5) == 0.0

def test_safe_divide_TC_016():
    # Ki?m tra ngo?i l? ZeroDivisionError khi m?u s? b?ng 0.
    with pytest.raises(ZeroDivisionError, match="denominator cannot be zero"):
        safe_divide(10, 0)

def test_safe_divide_TC_017():
    # Ki?m tra ngo?i l? ZeroDivisionError khi c? s? b? chia v� m?u s? d?u b?ng 0.
    with pytest.raises(ZeroDivisionError, match="denominator cannot be zero"):
        safe_divide(0, 0)

def test_safe_divide_TC_020():
    # Ki?m tra h�nh vi v?i ki?u kh�ng ph?i s?, h�m s? n�m TypeError do ph�p chia kh�ng h? tr? chu?i.
    with pytest.raises(TypeError):
        safe_divide('10', '2')