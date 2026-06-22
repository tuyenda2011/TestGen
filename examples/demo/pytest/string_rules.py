def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    cleaned = " ".join(name.strip().split())
    if not cleaned:
        raise ValueError("name cannot be empty")
    return cleaned.title()


def truncate(text: str, max_length: int) -> str:
    if max_length < 0:
        raise ValueError("max_length cannot be negative")
    if len(text) <= max_length:
        return text
    if max_length <= 3:
        return "." * max_length
    return text[: max_length - 3] + "..."


def count_ascii_vowels(text: str) -> int:
    vowels = set("aeiouAEIOU")
    return sum(1 for character in text if character in vowels)
