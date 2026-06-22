def letter_grade(score: float) -> str:
    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def is_passing(score: float, passing_score: float = 60) -> bool:
    if passing_score < 0 or passing_score > 100:
        raise ValueError("passing score must be between 0 and 100")
    return score >= passing_score


def grade_points(letter: str) -> float:
    points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
    normalized = letter.upper()
    if normalized not in points:
        raise ValueError("unknown grade letter")
    return points[normalized]
