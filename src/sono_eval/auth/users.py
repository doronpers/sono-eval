"""User models and mock database."""

from typing import Dict, Optional

from pydantic import BaseModel

from sono_eval.auth.keys import get_password_hash


class User(BaseModel):
    """User model."""

    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """User in database with hashed password."""

    hashed_password: str


# Types for type hinting
UserDb = Dict[str, UserInDB]


# Mock user database
# In a real app, this would be in a DB.
# For now, we seed one admin user.
# Password is "secret" (hashed)
FAKE_USERS_DB: UserDb = {
    "admin": UserInDB(
        username="admin",
        email="admin@example.com",
        disabled=False,
        hashed_password=get_password_hash("secret"),
    )
}


def get_user(db: UserDb, username: str) -> Optional[UserInDB]:
    """Get user by username."""
    if username in db:
        return db[username]
    return None
