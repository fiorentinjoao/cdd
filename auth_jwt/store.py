from .models import User
from .security import hash_password

users: dict[str, User] = {
    "user@example.com": User(
        id="1",
        email="user@example.com",
        hashed_password=hash_password("secret"),
    )
}

refresh_tokens: set[str] = set()


def get_user_by_email(email: str) -> User | None:
    return users.get(email)


def add_refresh_token(token: str) -> None:
    refresh_tokens.add(token)


def revoke_refresh_token(token: str) -> None:
    refresh_tokens.discard(token)


def is_refresh_token_valid(token: str) -> bool:
    return token in refresh_tokens
