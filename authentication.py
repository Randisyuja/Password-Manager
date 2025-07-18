import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from constants import SALT_PATH, MASTER_FILE


def generate_salt(path=SALT_PATH):
    if not os.path.exists(path):
        salt = os.urandom(16)
        with open(path, "wb") as f:
            f.write(salt)
    else:
        with open(path, "rb") as f:
            salt = f.read()
    return salt


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def save_master_password(password: str):
    salt = generate_salt()
    key = derive_key(password, salt)
    with open(MASTER_FILE, "wb") as f:
        f.write(key)


def validate_master_password(input_password: str) -> bool:
    if not os.path.exists(MASTER_FILE):
        return False
    salt = generate_salt()
    key = derive_key(input_password, salt)
    with open(MASTER_FILE, "rb") as f:
        stored_key = f.read()
    return key == stored_key
