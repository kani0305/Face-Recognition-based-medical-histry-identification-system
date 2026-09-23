import os
from cryptography.fernet import Fernet

KEY_DIR = "data"
KEY_FILE = os.path.join(KEY_DIR, "secret.key")


def generate_key():
    """Generate and save a new encryption key"""
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"Encryption key generated and saved to {KEY_FILE}")


def load_key():
    """Load the previously generated key"""
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()


def encrypt_data(data: str):
    """Encrypt a string"""
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())


def decrypt_data(encrypted_data: bytes):
    """Decrypt encrypted data"""
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()
