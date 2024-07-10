import datetime
import os
from datetime import timedelta
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.errors import AppServiceError, UnauthorizedError
from src.ops import ops_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/signin")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours


def _get_secret_key():
    return os.environ.get("JWT_SECRET_KEY")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates an access token and encodes it using a secret key and signature."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "token_type": "access"})
    encoded_jwt = jwt.encode(to_encode, _get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates an refresh token and encodes it using a secret key and signature."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire, "token_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, _get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt


def decode_refresh_token(encoded_jwt):
    """Decodes the encoded_jwt using the secret key."""
    try:
        payload = jwt.decode(encoded_jwt, _get_secret_key(), algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise UnauthorizedError("Invalid refresh token")
        token_type = payload.get("token_type")
        if token_type != "refresh":
            raise UnauthorizedError("Invalid refresh token")
        return payload
    except jwt.ExpiredSignatureError as ese:
        raise UnauthorizedError("The refresh token has expired") from ese
    except JWTError as jwt_err:
        raise UnauthorizedError("Invalid refresh token") from jwt_err


def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """Gets the currently authenticated user. This is used as part of
    verifying the token."""

    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise UnauthorizedError("Invalid access token")
        token_type = payload.get("token_type")
        if token_type != "access":
            raise UnauthorizedError("Invalid access token")
    except jwt.ExpiredSignatureError as ese:
        raise UnauthorizedError("The access token has expired") from ese
    except JWTError as jwt_err:
        raise UnauthorizedError("Invalid access token") from jwt_err

    user_coroutine = ops_user.get_user_by_email(db, email)
    if not user_coroutine:
        raise AppServiceError(
            "Expected to retrieve a valid user coroutine but this was not the case.",
            {"msg": f"email={email}"},
        )
    return user_coroutine
