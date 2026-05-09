from pwdlib import PasswordHash

# Initialize the password hash helper
password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a stored hash."""
    return password_hash.verify(plain_password, hashed_password)
