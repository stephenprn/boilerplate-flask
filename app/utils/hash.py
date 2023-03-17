import hashlib
import os
from base64 import b64encode
from typing import Tuple


def hash_password(password: str) -> Tuple[str, str]:
    salt = str(b64encode(os.urandom(32)))

    password_hashed = _hash_pw_salt(password=password, salt=salt)

    return password_hashed, salt


def check_password(password_input: str, salt: str, password_hashed: str) -> bool:
    pw_input_hashed = _hash_pw_salt(password=password_input, salt=salt)

    return password_hashed == pw_input_hashed


def _hash_pw_salt(password: str, salt: str) -> str:
    return str(
        b64encode(
            hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),  # Convert the password to bytes
                salt.encode("utf-8"),
                100000,
            )
        )
    )
