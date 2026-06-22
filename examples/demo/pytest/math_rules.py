def factorial(n: int) -> int:
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for value in range(2, n + 1):
        result *= value
    return result


def clamp(value: float, minimum: float, maximum: float) -> float:
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        raise ZeroDivisionError("denominator cannot be zero")
    return numerator / denominator
