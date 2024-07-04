from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src import oauth2
from src.db.database import get_db
from src.ops import ops_user
from src.routers.rt_exceptions import create_item_not_found_exception
from src.utils import hash

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def get_token(
    response: Response,
    request: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await ops_user.get_user_by_username(db, request.username)
    if not user:
        raise create_item_not_found_exception(message="Invalid credentials")
    if not hash.verify_bcrypt(request.password, user.password_hash):
        raise create_item_not_found_exception(message="Invalid credentials")
    access_token = oauth2.create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }
