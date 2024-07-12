from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src import oauth2
from src.common.database import get_db
from src.errors import UnauthorizedError
from src.ops import ops_user
from src.utils import hash as h

router = APIRouter(prefix="/api/users", tags=["users"])


# @router.post("/signin")
# async def signin(
#     # response: Response,
#     request: SchemaSignin,
#     db: AsyncSession = Depends(get_db),
# ):


@router.post("/signin")
async def signin(
    # response: Response,
    request: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await ops_user.get_user_by_email(db, request.username)
    if not user:
        raise UnauthorizedError("Invalid credentials")
    if not h.verify_bcrypt(request.password, user.password_hash):
        raise UnauthorizedError("Invalid credentials")
    access_token = oauth2.create_access_token(
        data={
            "sub": user.email,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_id": str(user.id),
        }
    )
    refresh_token = oauth2.create_refresh_token(
        data={
            "sub": user.email,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_id": str(user.id),
        }
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "email": user.email,
    }
