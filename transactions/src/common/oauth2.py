import datetime
import os
from datetime import timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/api/users/signin")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _get_secret_key():
    return os.environ.get("JWT_SECRET_KEY")


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    expire_mins=ACCESS_TOKEN_EXPIRE_MINUTES,
):
    """Creates an access token and encodes it using a secret key and signature."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(
            minutes=expire_mins
        )
    to_encode.update({"exp": expire, "token_type": "access"})
    encoded_jwt = jwt.encode(to_encode, _get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt


def _build_http_exc_401(
    detail,
):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_user_from_access_token(token: str = Depends(oauth2_scheme)):
    """Gets the currently authenticated user via that access token.
    This is used as part of verifying the token."""

    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise _build_http_exc_401("Invalid access token")
        token_type = payload.get("token_type")
        if token_type != "access":
            raise _build_http_exc_401("Invalid access token")
        first_name: str = payload.get("first_name")
        last_name: str = payload.get("last_name")
        user_id: str = payload.get("user_id")
    except jwt.ExpiredSignatureError as ese:
        raise _build_http_exc_401(detail="The access token has expired") from ese
    except JWTError as jwt_err:
        raise _build_http_exc_401("Invalid access token") from jwt_err

    return {
        "id": user_id,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }
