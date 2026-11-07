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
