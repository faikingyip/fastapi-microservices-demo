from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.srv_layer import services
from src.common.ctx.api_context import ApiContext
from src.utils import oauth2

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/signin")
async def signin(
    # response: Response,
    req: OAuth2PasswordRequestForm = Depends(),
    api_ctx: ApiContext = Depends(
        ApiContext.get_instance_async,
    ),
):
    try:
        user = await services.signin(
            req.username,
            req.password,
            api_ctx.uow,
        )
    except services.InvalidCredentialsError as ice:
        raise services.build_http_exc_401(
            "Invalid credentials",
        ) from ice

    data = services.build_token_data(
        str(user.id),
        user.email,
        user.first_name,
        user.last_name,
    )
    access_token = oauth2.create_access_token(data)
    refresh_token = oauth2.create_refresh_token(data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "email": user.email,
    }
