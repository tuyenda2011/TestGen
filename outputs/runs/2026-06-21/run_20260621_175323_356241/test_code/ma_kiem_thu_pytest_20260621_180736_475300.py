# ===== Tests for letter_grade =====
from source_under_test import letter_grade
import pytest

# Kiểm tra các ký tự điểm cho các điểm số hợp lệ
@pytest.mark.parametrize("score,expected", [
    (95, "A"),   # Điểm >= 90 trả về A
    (90, "A"),   # Biên giới điểm 90 trả về A
    (85, "B"),   # Điểm >= 80 trả về B
    (80, "B"),   # Biên giới điểm 80 trả về B
    (75, "C"),   # Điểm >= 70 trả về C
    (70, "C"),   # Biên giới điểm 70 trả về C
    (65, "D"),   # Điểm >= 60 trả về D
    (60, "D"),   # Biên giới điểm 60 trả về D
    (55, "F"),   # Điểm < 60 trả về F
    (0, "F"),    # Biên giới điểm 0 trả về F
])
def test_letter_grade_valid_scores(score, expected):
    # Kiểm tra hàm trả về đúng ký tự điểm dựa trên nguồn logic
    assert letter_grade(score) == expected

# Kiểm tra ngoại lệ cho điểm số nằm ngoài khoảng cho phép
@pytest.mark.parametrize("invalid_score", [-5, -1, 101, 150])
def test_letter_grade_invalid_scores(invalid_score):
    # Kiểm tra hàm ném ValueError khi điểm < 0 hoặc điểm > 100
    with pytest.raises(ValueError, match="score must be between 0 and 100"):
        letter_grade(invalid_score)

# ===== Tests for is_passing =====
from source_under_test import is_passing

# Kiểm tra trường hợp điểm đạt và vượt qua mức điểm chuẩn
@pytest.mark.parametrize("score,passing_score,expected", [
    (80, 70, True),   # Điểm 80 >= 70 trả về True
    (70, 70, True),   # Điểm bằng mức chuẩn trả về True
    (100, 60, True),  # Điểm cao nhất vẫn trả về True
])
def test_is_passing_true_cases(score, passing_score, expected):
    # Kiểm tra hàm trả về True khi điểm >= mức điểm chuẩn
    assert is_passing(score, passing_score) == expected

# Kiểm tra trường hợp điểm dưới mức điểm chuẩn
@pytest.mark.parametrize("score,passing_score", [(50, 60), (60, 70), (69, 70)])
def test_is_passing_false_cases(score, passing_score):
    # Kiểm tra hàm trả về False khi điểm < mức điểm chuẩn
    assert is_passing(score, passing_score) == False

# Kiểm tra ngoại lệ cho mức điểm chuẩn không hợp lệ
@pytest.mark.parametrize("passing_score", [-10, -1, 101, 150])
def test_is_passing_invalid_passing_score(passing_score):
    # Kiểm tra hàm ném ValueError khi passing_score < 0 hoặc > 100
    with pytest.raises(ValueError, match="passing score must be between 0 and 100"):
        is_passing(80, passing_score)

# ===== Tests for grade_points =====
from source_under_test import grade_points

# Kiểm tra điểm số tương ứng với các ký tự điểm
@pytest.mark.parametrize("letter,expected", [
    ("A", 4.0),   # Ký tự A trả về 4.0
    ("B", 3.0),   # Ký tự B trả về 3.0
    ("C", 2.0),   # Ký tự C trả về 2.0
    ("D", 1.0),   # Ký tự D trả về 1.0
    ("F", 0.0),   # Ký tự F trả về 0.0
])
def test_grade_points_valid_letters(letter, expected):
    # Kiểm tra hàm trả về đúng điểm số dựa trên nguồn logic
    assert grade_points(letter) == expected

# Kiểm tra hàm xử lý chữ thường bằng cách chuyển thành chữ hoa
def test_grade_points_lowercase_letter():
    # Kiểm tra hàm chuyển đổi chữ thường thành chữ hoa và trả về đúng điểm
    assert grade_points("a") == 4.0
    assert grade_points("c") == 2.0

# Kiểm tra ngoại lệ cho ký tự điểm không tồn tại
@pytest.mark.parametrize("invalid_letter", ["Z", "X", "G", "1", ""])
def test_grade_points_invalid_letter(invalid_letter):
    # Kiểm tra hàm ném ValueError khi ký tự không nằm trong từ điển điểm
    with pytest.raises(ValueError, match="unknown grade letter"):
        grade_points(invalid_letter)