"""Security utilities for authentication."""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from sono_eval.utils.config import get_config

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
config = get_config()

# Security Configurations
ALGORITHM = getattr(config, "jwt_algorithm", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(config, "access_token_expire_minutes", 30)
API_KEY_PREFIX = getattr(config, "api_key_prefix", "se_")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default 7 days for refresh token
        expire = datetime.now(timezone.utc) + timedelta(days=7)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def generate_api_key() -> str:
    """Generate a secure API key."""
    return f"{API_KEY_PREFIX}{secrets.token_urlsafe(32)}"


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage."""
    return pwd_context.hash(api_key)


def verify_api_key_hash(plain_api_key: str, hashed_key: str) -> bool:
    """Verify an API key against its hash."""
    return pwd_context.verify(plain_api_key, hashed_key)
