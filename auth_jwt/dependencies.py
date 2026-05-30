from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .models import User
from .security import decode_token
from .store import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    token_data = decode_token(token)
    if token_data.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token_invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(token_data.sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token_invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
