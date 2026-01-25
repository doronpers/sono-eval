"""Authentication models."""

from datetime import datetime, timezone
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# SQLAlchemy Models
class UserDB(Base):
    """User database model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    api_keys = relationship("APIKeyDB", back_populates="user")


class APIKeyDB(Base):
    """API Key database model."""

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    user = relationship("UserDB", back_populates="api_keys")


# Pydantic Models for API
class Token(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    """Token payload data."""

    email: Optional[str] = None
    user_id: Optional[int] = None


class UserBase(BaseModel):
    """User base model."""

    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """User creation model."""

    password: str


class UserUpdate(UserBase):
    """User update model."""

    password: Optional[str] = None


class User(UserBase):
    """User public model."""

    id: int
    is_superuser: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class APIKeyCreate(BaseModel):
    """API Key creation model."""

    name: str = Field(..., min_length=1, max_length=50)
    expires_in_days: Optional[int] = Field(None, ge=1, le=365)


class APIKeyResponse(BaseModel):
    """API Key response model (includes secret key only on creation)."""

    id: int
    name: str
    key: Optional[str] = None  # Only returned once
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True


class APIKeyList(BaseModel):
    """API Key list model (no secrets)."""

    id: int
    name: str
    created_at: datetime
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True
