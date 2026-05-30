from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    hashed_password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str
    type: str  # "access" | "refresh"
