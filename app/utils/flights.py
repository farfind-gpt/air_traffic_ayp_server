from app.utils.airlines import is_valid_airline_code


def is_valid_flight_code(string: str) -> bool:
    """
    checks if given string is a valid flight code,
    returns True if it is, False otherwise

    flight code format: "AAA-NNNN",
    where A is any latin upper letter and N is digit
    """

    if not isinstance(string, str):
        return False

    splitted = string.split('-')

    if len(splitted) != 2:
        return False

    if not is_valid_airline_code(splitted[0]):
        return False

    if not splitted[1].isdigit():
        return False

    return True

def parse_flight_code(string: str) -> tuple[str, int] | None:
    """
    parses given flight code and returns tuple where
    the first element is airline code and the second is
    flight number

    returns None if given string is not a valid flight code

    flight code format: "AAA-NNNN",
    where A is any latin upper letter and N is digit
    """

    if not is_valid_flight_code(string):
        return None

    splitted = string.split('-')

    return splitted[0], int(splitted[1])

def build_flight_code(airline_code: str, flight_number: int) -> str | None:
    """
    builds flight code string
    returns None if given data is invalid

    flight code format: "AAA-NNNN",
    where A is any latin upper letter and N is digit
    """

    if not (isinstance(airline_code, str) and isinstance(flight_number, int)):
        return None

    if not is_valid_airline_code(airline_code) or not (0 <= flight_number <= 9999):
        return None

    return f"{airline_code}-{flight_number:04}"
