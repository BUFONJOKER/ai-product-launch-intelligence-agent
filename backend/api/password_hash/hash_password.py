from pwdlib import PasswordHash

# Initialize the password hash helper
password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    """Generates a secure hash from a plain-text password."""
    return password_hash.hash(password)
