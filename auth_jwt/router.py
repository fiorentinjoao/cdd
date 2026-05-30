from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from .config import settings
from .models import LoginRequest, TokenPair, User
from .dependencies import get_current_user
from .security import create_token, decode_token, verify_password
from .store import (
    add_refresh_token,
    get_user_by_email,
    is_refresh_token_valid,
    revoke_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _build_token_pair(email: str) -> TokenPair:
    access_token = create_token(
        {"sub": email, "type": "access"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_token(
        {"sub": email, "type": "refresh"},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    add_refresh_token(refresh_token)
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=TokenPair)
def login(body: LoginRequest) -> TokenPair:
    user = get_user_by_email(body.email)
    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_credentials",
        )
    return _build_token_pair(user.email)


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest) -> TokenPair:
    if not is_refresh_token_valid(body.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh_token_invalid",
        )
    token_data = decode_token(body.refresh_token)
    if token_data.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh_token_invalid",
        )
    revoke_refresh_token(body.refresh_token)
    return _build_token_pair(token_data.sub)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(body: RefreshRequest, _: User = Depends(get_current_user)) -> None:
    revoke_refresh_token(body.refresh_token)
