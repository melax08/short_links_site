import random

from .constants import ALLOWED_CHARACTERS, RANDOM_SHORT_LINK_LEN
from .models import URLMap


def get_unique_short_id() -> str:
    """Return random string with latin letters and numbers."""
    allowed_characters = list(ALLOWED_CHARACTERS)
    random_id = ''.join(random.choices(
        allowed_characters, k=RANDOM_SHORT_LINK_LEN))
    while URLMap.query.filter_by(short=random_id).first() is not None:
        random_id = ''.join(random.choices(
            allowed_characters, k=RANDOM_SHORT_LINK_LEN))
    return random_id


def validate_short_link(data: str) -> bool:
    """Validate short link, if there are unresolved characters in the string,
    it returns False. If string contains only allowed
    characters - returns True."""
    for symbol in data:
        if symbol not in ALLOWED_CHARACTERS:
            return False
    return True
