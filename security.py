import os
from cryptography.fernet import Fernet
from passlib.hash import pbkdf2_sha256
import hmac
import hashlib
from pathlib import Path

FERNET_KEY_FILE = os.environ.get('FERNET_KEY_FILE', 'fernet.key')
HMAC_KEY_FILE = os.environ.get('HMAC_KEY_FILE', 'hmac.key')

def load_or_create_fernet_key(file_path: str = FERNET_KEY_FILE):
    # Prefer env var FERNET_KEY if set
    env_key = os.environ.get('FERNET_KEY')
    if env_key:
        return env_key.encode()
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    key = Fernet.generate_key()
    with open(file_path, 'wb') as f:
        f.write(key)
    return key

def get_fernet():
    key = load_or_create_fernet_key()
    return Fernet(key)

def load_or_create_hmac_key(file_path: str = HMAC_KEY_FILE) -> bytes:
    env_key = os.environ.get('HMAC_KEY')
    if env_key:
        return env_key.encode()
    p = Path(file_path)
    if p.exists():
        return p.read_bytes()
    key = hashlib.sha256(Fernet.generate_key()).digest()
    p.write_bytes(key)
    return key

def compute_hmac(key: bytes, message: str) -> str:
    return hmac.new(key, message.encode('utf-8'), hashlib.sha256).hexdigest()

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, pw_hash: str) -> bool:
    try:
        return pbkdf2_sha256.verify(password, pw_hash)
    except Exception:
        return False
