"""Authentication dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError

from sono_eval.auth.jwt import decode_token
from sono_eval.auth.users import FAKE_USERS_DB, User, get_user
from sono_eval.utils.config import get_config

config = get_config()

# Token URL must match the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Get current user from token.

    Validates the token and retrieves user from DB.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(FAKE_USERS_DB, username)
    if user is None:
        raise credentials_exception

    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user
