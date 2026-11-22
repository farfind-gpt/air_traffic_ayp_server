from app.models.passenger import Passenger


def get_passport_id_string(passanger: Passenger) -> str:
    """
    returns passport's series and number as string.
    format: "SSSS-NNNNNN"
    """
    return f"{passanger.series:04}-{passanger.number:06}"

def validate_seires_and_number_format(string: str) -> bool:
    """
    returns True if given string matches passport's series and number format
    ("SSSS-NNNNNN", where all S and N are digits)
    """
    splitted: list[str] = string.split('-')
    return len(splitted) == 2 \
           and len(splitted[0]) == 4 and len(splitted[1]) == 6 \
           and splitted[0].isdigit() and splitted[1].isdigit()

def get_series_and_number_from_string(string: str) -> tuple[int, int] | None:
    """
    returns passport series and number from given string
    as tuple with 2 int values (first is series, second is number),
    or None if string has invalid format. correct format is
    "SSSS-NNNNNN", where all S and N are digits
    """
    if not validate_seires_and_number_format(string):
        return None

    splitted: list[str] = string.split('-')

    return (int(splitted[0]), int(splitted[1]))
