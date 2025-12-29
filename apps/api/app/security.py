import base64
import secrets
from typing import Optional

from cryptography.fernet import Fernet

from app.config import settings

_fernet: Optional[Fernet] = None


def _build_fernet() -> Fernet:
    if not settings.token_encryption_key:
        raise RuntimeError("TOKEN_ENCRYPTION_KEY is required")
    raw_key = settings.token_encryption_key.encode("utf-8")
    try:
        base64.urlsafe_b64decode(raw_key)
        key = raw_key
    except Exception:
        key = base64.urlsafe_b64encode(raw_key.ljust(32, b"0")[:32])
    return Fernet(key)


def get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        _fernet = _build_fernet()
    return _fernet


def encrypt_value(value: str) -> str:
    return get_fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_value(value: str) -> str:
    return get_fernet().decrypt(value.encode("utf-8")).decode("utf-8")


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)
