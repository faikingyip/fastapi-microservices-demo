from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import datetime
from datetime import timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.ops.ops_user import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token'

)

SECRET_KEY = 'd69816079fc14f65dfd3a94aa41739eef5590abc35e2c7961a0c50a02e9ff134'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
  else:
    expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
       raise credentials_exception
    return user
       

