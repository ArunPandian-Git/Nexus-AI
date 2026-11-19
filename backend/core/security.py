from pathlib import Path

Path("/content/backend/core").mkdir(
    parents=True,
    exist_ok=True
)

Path("/content/backend/core/__init__.py").touch()

%%writefile /content/backend/core/security.py

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from backend.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict) -> str:

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        settings.secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str):

    return jwt.decode(
        token,
        settings.secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm]
    )
