from random import randint


_allowed_characters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

def generate_reservation_group_code() -> str:
    """
    returns random reservation group code,
    a string of 5 or 6 characters, every of which
    can be upper-case latin letter or digit.

    for example: "GH9DI0"
    """

    ret = ""

    for _ in range(5 + randint(0, 1)):
        ret += _allowed_characters[randint(0, len(_allowed_characters)-1)]

    return ret

def is_valid_reservation_group_code(string: str) -> bool:
    """
    checks if given string is valid reservation group id.
    returns True if it is, otherwise False.

    reservation group id is a string of 5 or 6 characters,
    every of which can be upper-case latin letter or digit.

    for example: "GH9DI0"
    """

    if not isinstance(string, str):
        return False

    if len(string) != 6:
        return False

    for c in string:
        if c not in _allowed_characters:
            return False

    return True


__all__ = ["generate_reservation_group_code", "is_valid_reservation_group_code"]
