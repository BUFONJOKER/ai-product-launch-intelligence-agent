from pwdlib import PasswordHash

# Initialize the password hash helper
password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    """Generate a secure hash from a plain-text password.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The cryptographic password hash suitable for storage.
    """
    return password_hash.hash(password)
