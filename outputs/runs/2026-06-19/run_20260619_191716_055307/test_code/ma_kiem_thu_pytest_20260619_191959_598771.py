# ===== Tests for letter_grade =====
from source_under_test import letter_grade
import pytest

def test_letter_grade_negative_score_tc001():
    """Ki?m tra h�m letter_grade n�m ValueError khi di?m < 0."""
    with pytest.raises(ValueError) as exc_info:
        letter_grade(-5)
    assert str(exc_info.value) == "score must be between 0 and 100"

def test_letter_grade_over_score_tc002():
    """Ki?m tra h�m letter_grade n�m ValueError khi di?m > 100."""
    with pytest.raises(ValueError) as exc_info:
        letter_grade(105)
    assert str(exc_info.value) == "score must be between 0 and 100"

def test_letter_grade_score_95_tc003():
    """Ki?m tra h�m letter_grade tr? v? 'A' cho di?m 95."""
    assert letter_grade(95) == "A"

def test_letter_grade_score_85_tc004():
    """Ki?m tra h�m letter_grade tr? v? 'B' cho di?m 85."""
    assert letter_grade(85) == "B"

def test_letter_grade_score_75_tc005():
    """Ki?m tra h�m letter_grade tr? v? 'C' cho di?m 75."""
    assert letter_grade(75) == "C"

def test_letter_grade_score_65_tc006():
    """Ki?m tra h�m letter_grade tr? v? 'D' cho di?m 65."""
    assert letter_grade(65) == "D"

def test_letter_grade_score_59_tc007():
    """Ki?m tra h�m letter_grade tr? v? 'F' cho di?m 59."""
    assert letter_grade(59) == "F"

# ===== Tests for is_passing =====
from source_under_test import is_passing

def test_is_passing_negative_passing_score_tc008():
    """Ki?m tra h�m is_passing n�m ValueError khi passing_score < 0."""
    with pytest.raises(ValueError) as exc_info:
        is_passing(50, -10)
    assert str(exc_info.value) == "passing score must be between 0 and 100"

def test_is_passing_over_passing_score_tc009():
    """Ki?m tra h�m is_passing n�m ValueError khi passing_score > 100."""
    with pytest.raises(ValueError) as exc_info:
        is_passing(50, 110)
    assert str(exc_info.value) == "passing score must be between 0 and 100"

def test_is_passing_true_when_meets_tc010():
    """Ki?m tra h�m is_passing tr? v? True khi score >= passing_score."""
    assert is_passing(80, 70) is True

def test_is_passing_false_when_below_tc011():
    """Ki?m tra h�m is_passing tr? v? False khi score < passing_score."""
    assert is_passing(65, 70) is False

# ===== Tests for grade_points =====
from source_under_test import grade_points

def test_grade_points_A_tc012():
    """Ki?m tra h�m grade_points tr? v? 4.0 cho ch? 'A'."""
    assert grade_points("A") == 4.0

def test_grade_points_F_tc013():
    """Ki?m tra h�m grade_points tr? v? 0.0 cho ch? 'F'."""
    assert grade_points("F") == 0.0

def test_grade_points_unknown_letter_tc014():
    """Ki?m tra h�m grade_points n�m ValueError khi ch? kh�ng h?p l?."""
    with pytest.raises(ValueError) as exc_info:
        grade_points("Z")
    assert str(exc_info.value) == "unknown grade letter"