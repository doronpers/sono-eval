"""Authentication routes."""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from sono_eval.auth.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from sono_eval.auth.keys import verify_password
from sono_eval.auth.users import FAKE_USERS_DB, get_user
from sono_eval.utils.audit import log_auth_attempt

router = APIRouter()


class Token(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    Login to get access token.

    Username: admin
    Password: secret
    """
    user = get_user(FAKE_USERS_DB, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        # Log failure
        log_auth_attempt(
            user_id=form_data.username,
            success=False,
            ip_address="unknown",  # We don't have request here easily without request arg
            reason="invalid_credentials",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Log success
    log_auth_attempt(
        user_id=user.username, success=True, ip_address="unknown", method="password"
    )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
