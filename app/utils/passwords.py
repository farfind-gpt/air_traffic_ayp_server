from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from typing import Literal


ph: PasswordHasher = PasswordHasher()


def hash(password: str) -> str:
    """
    takes plain text password and returns hashed one
    (argon2 is used)
    """
    return ph.hash(password)

def verify(plain: str, hashed: str) -> bool:
    """
    takes plain text and hashed (with salt specified) passwords and
    returns True if hashing given plain text password with salt
    from hashed one will produce the same hash, False otherwise
    (argon2 is used)
    """
    try:
        return ph.verify(hashed, plain)
    except VerifyMismatchError, VerificationError, InvalidHashError:
        return False

def is_weak(password: str) -> str | Literal[False]:
    """
    checks if given password is weak.
    returns False if it is strong and non-empty
    string with description why it is weak otherwise

    passwords are considered strong if they have at least
    8 characters total and at least 5 unique characters
    """
    if len(password) < 8:
        return "password is too short, minimal length is 8 characters"
    elif len(set(password)) < 5:
        return "password is too weak, should have at least 5 unique characters"
    else:
        return False
