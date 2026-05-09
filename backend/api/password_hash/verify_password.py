from pwdlib import PasswordHash

# Initialize the password hash helper
password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored hash value.

    Args:
        plain_password (str): The plain-text password provided by a user.
        hashed_password (str): The previously stored password hash.

    Returns:
        bool: `True` if the password matches the hash; otherwise `False`.
    """
    return password_hash.verify(plain_password, hashed_password)
