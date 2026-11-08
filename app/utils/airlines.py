"""
returns True if given string is valid airline code, False otherwise.
valid airline code is 3 uppercase latin letters, like "ABC"
"""
def is_valid_airline_code(string: str) -> bool:
    if len(string) != 3:
        return False

    symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for c in string:
        if c not in symbols:
            return False

    return True
