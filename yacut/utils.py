from .constants import ALLOWED_CHARACTERS


def validate_short_link(data: str) -> bool:
    """Validate short link, if there are unresolved characters in the string,
    it returns False. If string contains only allowed
    characters - returns True."""
    for symbol in data:
        if symbol not in ALLOWED_CHARACTERS:
            return False
    return True
