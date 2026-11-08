# TODO check country codes
"""
checks if given string is valid ICAO index.
if it is, returns True, else False.
"""
def is_valid_icao_index(string: str) -> bool:
    if len(string) != 4:
        return False

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for c in string:
        if c not in letters:
            return False

    return True
