"""JWT token management."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from sono_eval.utils.config import get_config

# Config access
config = get_config()

# Constants
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new access token.

    Args:
        data: Payload data (e.g. {"sub": "user_id"})
        expires_delta: Optional expiration time
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    # Create token
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and verify a token.

    Returns:
        Payload dict if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
