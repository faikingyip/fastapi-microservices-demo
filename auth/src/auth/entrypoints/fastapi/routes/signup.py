import json

from fastapi import APIRouter, Depends, status

from src.auth.entrypoints.fastapi import schemas
from src.auth.srv_layer import services
from src.auth.srv_layer.uow import SqlAlchemyUoW
from src.common.ctx.api_context import ApiContext
from src.event.publishers.user_created_publisher import UserCreatedPublisher

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/signup",
    response_model=schemas.SchemaUserDisplay,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user.",
)
async def signup(
    req: schemas.SchemaUserCreate,
    api_ctx: ApiContext = Depends(
        ApiContext.get_instance_async,
    ),
):
    user = await services.signup(
        req.email,
        req.password,
        req.first_name,
        req.last_name,
        SqlAlchemyUoW(api_ctx.db_man.session_local),
    )

    with api_ctx.msg_pub_client:
        UserCreatedPublisher(api_ctx.msg_pub_client).publish(
            json.dumps(
                {
                    "user_id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            )
        )
    return user
