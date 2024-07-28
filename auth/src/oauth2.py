import datetime
import os
from datetime import timedelta
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.auth.srv_layer import services
from src.auth.srv_layer.uow import SqlAlchemyUoW
from src.common.ctx.api_context import ApiContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/signin")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours


def _get_secret_key():
    return os.environ.get("JWT_SECRET_KEY")


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    expire_mins=ACCESS_TOKEN_EXPIRE_MINUTES,
):
    """Creates an access token and encodes it
    using a secret key and signature."""
    to_encode = data.copy()
    if expires_delta:
        expire = (
            datetime.datetime.now(
                datetime.timezone.utc,
            )
            + expires_delta
        )
    else:
        expire = datetime.datetime.now(
            datetime.timezone.utc,
        ) + timedelta(minutes=expire_mins)
    to_encode.update({"exp": expire, "token_type": "access"})
    encoded_jwt = jwt.encode(
        to_encode,
        _get_secret_key(),
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    expire_mins=REFRESH_TOKEN_EXPIRE_MINUTES,
):
    """Creates an refresh token and encodes it
    using a secret key and signature."""
    to_encode = data.copy()
    if expires_delta:
        expire = (
            datetime.datetime.now(
                datetime.timezone.utc,
            )
            + expires_delta
        )
    else:
        expire = datetime.datetime.now(
            datetime.timezone.utc,
        ) + timedelta(minutes=expire_mins)
    to_encode.update({"exp": expire, "token_type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        _get_secret_key(),
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def decode_refresh_token(encoded_jwt):
    """Decodes the encoded_jwt using the secret key."""
    try:
        payload = jwt.decode(
            encoded_jwt,
            _get_secret_key(),
            algorithms=[ALGORITHM],
        )
        email = payload.get("sub")
        if not email:
            raise services.build_http_exc_401("Invalid refresh token")
        token_type = payload.get("token_type")
        if token_type != "refresh":
            raise services.build_http_exc_401("Invalid refresh token")
        return payload
    except jwt.ExpiredSignatureError as ese:
        raise services.build_http_exc_401("The refresh token has expired") from ese
    except JWTError as jwt_err:
        raise services.build_http_exc_401("Invalid refresh token") from jwt_err


def get_current_user(
    token: str = Depends(oauth2_scheme),
    api_ctx: ApiContext = Depends(ApiContext.get_instance_async),
):
    """Gets the currently authenticated user. This is used as part of
    verifying the token."""

    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise services.build_http_exc_401("Invalid access token")
        token_type = payload.get("token_type")
        if token_type != "access":
            raise services.build_http_exc_401("Invalid access token")
    except jwt.ExpiredSignatureError as ese:
        raise services.build_http_exc_401(
            detail="The access token has expired",
        ) from ese
    except JWTError as jwt_err:
        raise services.build_http_exc_401("Invalid access token") from jwt_err

    user_coroutine = services.get_by_email(
        email,
        SqlAlchemyUoW(api_ctx.db_man.session_local),
    )
    if not user_coroutine:
        raise services.build_http_exc_401("Invalid access token")
    return user_coroutine
