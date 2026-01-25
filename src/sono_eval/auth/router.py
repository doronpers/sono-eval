"""Authentication router."""

from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from sono_eval.api.limiter import limiter
from sono_eval.utils.audit import log_audit_event, AuditEventType

# from . import models, schemas
from .dependencies import get_db, get_current_user, get_current_active_user
from .security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    generate_api_key,
    hash_api_key,
)

# Fix imports since we defined models in .models, creating schemas alias to avoid conflict
# Actually, I defined Pydantic models in models.py too.
# Let's import them properly.
from .models import (
    User as UserSchema,
    UserCreate,
    Token,
    APIKeyCreate,
    APIKeyResponse,
    APIKeyList,
    UserDB,
    APIKeyDB,
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserSchema)
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    log_audit_event(
        event_type=AuditEventType.REGISTER,
        user_id=str(db_user.id),
        ip_address=request.client.host if request.client else None,
        details={"email": user.email},
    )

    return db_user


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """OAuth2 compatible token login, retrieve an access token for future requests."""
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        log_audit_event(
            event_type=AuditEventType.LOGIN_FAILURE,
            ip_address=request.client.host if request.client else None,
            details={"email": form_data.username},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )

    log_audit_event(
        event_type=AuditEventType.LOGIN_SUCCESS,
        user_id=str(user.id),
        ip_address=request.client.host if request.client else None,
        details={"email": user.email},
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: UserSchema = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user


@router.post("/api-keys", response_model=APIKeyResponse)
def create_api_key(
    key_data: APIKeyCreate,
    current_user: UserDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new API Key."""
    plain_key = generate_api_key()
    key_hash = hash_api_key(plain_key)

    expires_at = None
    if key_data.expires_in_days:
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=key_data.expires_in_days
        )

    db_key = APIKeyDB(
        key_hash=key_hash,
        name=key_data.name,
        user_id=current_user.id,
        expires_at=expires_at,
        created_at=datetime.now(timezone.utc),
        is_active=True,
    )
    db.add(db_key)
    db.commit()
    db.refresh(db_key)

    # Return formatted response with plain key (only time it is shown)
    return APIKeyResponse(
        id=db_key.id,
        name=db_key.name,
        key=plain_key,
        created_at=db_key.created_at,
        expires_at=db_key.expires_at,
    )


@router.get("/api-keys", response_model=List[APIKeyList])
def list_api_keys(
    current_user: UserDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """List all API keys for current user."""
    keys = db.query(APIKeyDB).filter(APIKeyDB.user_id == current_user.id).all()
    return keys


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    key_id: int,
    current_user: UserDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Revoke (delete) an API Key."""
    key = (
        db.query(APIKeyDB)
        .filter(APIKeyDB.id == key_id, APIKeyDB.user_id == current_user.id)
        .first()
    )

    if not key:
        raise HTTPException(status_code=404, detail="API Key not found")

    db.delete(key)
    db.commit()
