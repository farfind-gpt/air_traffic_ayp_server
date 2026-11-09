from app.models.passport_info import PassportInfo


"""
returns passport's series and number as string.
format: "SSSS-NNNNNN"
"""
def get_id_string(passport_info: PassportInfo) -> str:
    return f"{passport_info.series:04}-{passport_info.number:06}"


"""
returns True if given string matches passport's series and number format
("SSSS-NNNNNN", where all S and N are digits)
"""
def validate_seires_and_number_format(string: str) -> bool:
    splitted: list[str] = string.split('-')
    return len(splitted) == 2 \
           and len(splitted[0]) == 4 and len(splitted[1]) == 6 \
           and splitted[0].isdigit() and splitted[1].isdigit()

"""
returns passport series and number from given string
as tuple with 2 int values (first is series, second is number),
or None if string has invalid format. correct format is
"SSSS-NNNNNN", where all S and N are digits
"""
def get_series_and_number_from_string(string: str) -> tuple[int, int] | None
    if not validate_seires_and_number_format(string):
        return None

    splitted: list[str] = string.split('-')

    return (int(splitted[0]), int(splitted[1]))
