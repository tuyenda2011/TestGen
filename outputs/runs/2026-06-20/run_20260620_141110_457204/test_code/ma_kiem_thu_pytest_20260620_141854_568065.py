# ===== Tests for letter_grade =====
from source_under_test import letter_grade

def test_letter_grade_TC_001():
    # Ki?m tra ngo?i l? khi score nh? hon 0.
    import pytest
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        letter_grade(-5)

def test_letter_grade_TC_002():
    # Ki?m tra ngo?i l? khi score l?n hon 100.
    import pytest
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        letter_grade(150)

def test_letter_grade_TC_003():
    # Ki?m tra tr? v? 'A' khi score >= 90.
    assert letter_grade(95) == "A"

def test_letter_grade_TC_004():
    # Ki?m tra tr? v? 'B' khi score >= 80 v� < 90.
    assert letter_grade(85) == "B"

def test_letter_grade_TC_005():
    # Ki?m tra tr? v? 'C' khi score >= 70 v� < 80.
    assert letter_grade(75) == "C"

def test_letter_grade_TC_006():
    # Ki?m tra tr? v? 'D' khi score >= 60 v� < 70.
    assert letter_grade(65) == "D"

def test_letter_grade_TC_007():
    # Ki?m tra tr? v? 'F' khi score < 60.
    assert letter_grade(55) == "F"

# ===== Tests for is_passing =====
from source_under_test import is_passing

def test_is_passing_TC_008():
    # Ki?m tra ngo?i l? khi passing_score nh? hon 0.
    import pytest
    with pytest.raises(ValueError, match="passing score must be between 0 and 100"):
        is_passing(50, -10)

def test_is_passing_TC_009():
    # Ki?m tra ngo?i l? khi passing_score l?n hon 100.
    import pytest
    with pytest.raises(ValueError, match="passing score must be between 0 and 100"):
        is_passing(50, 110)

def test_is_passing_TC_010():
    # Ki?m tra tr? v? True khi score d?t passing_score.
    assert is_passing(80, 70) == True

def test_is_passing_TC_011():
    # Ki?m tra tr? v? False khi score du?i passing_score.
    assert is_passing(60, 70) == False

# ===== Tests for grade_points =====
from source_under_test import grade_points

def test_grade_points_TC_012():
    # Ki?m tra tr? v? di?m s? tuong ?ng v?i ch? c�i 'A'.
    assert grade_points("A") == 4.0

def test_grade_points_TC_013():
    # Ki?m tra tr? v? di?m s? tuong ?ng v?i ch? c�i 'F'.
    assert grade_points("F") == 0.0

def test_grade_points_TC_014():
    # Ki?m tra ngo?i l? khi ch? c�i kh�ng h?p l?.
    import pytest
    with pytest.raises(ValueError, match="unknown grade letter"):
        grade_points("Z")