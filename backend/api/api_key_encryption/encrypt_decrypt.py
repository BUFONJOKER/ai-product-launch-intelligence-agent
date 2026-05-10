import os
from cryptography.fernet import Fernet
from config import ENCRYPTION_MASTER_KEY


MASTER_KEY = ENCRYPTION_MASTER_KEY
cipher_suite = Fernet(MASTER_KEY)

def encrypt_key(plain_api_key: str) -> str:
    """Encrypts the user's API key for storage."""
    return cipher_suite.encrypt(plain_api_key.encode()).decode()

def decrypt_key(encrypted_api_key: str) -> str:
    """Decrypts the key for use in an external request."""
    return cipher_suite.decrypt(encrypted_api_key.encode()).decode()
