import json

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.ctx.api_context import ApiContext
from src.event.publishers.user_created_publisher import UserCreatedPublisher
from src.ops import ops_user
from src.schemas.schema_user import SchemaUserCreate, SchemaUserDisplay

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/signup",
    response_model=SchemaUserDisplay,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user.",
)
async def signup(
    request: SchemaUserCreate,
    db: AsyncSession = Depends(ApiContext.get_instance().db_man.get_session),
    rmq_pub_client=Depends(ApiContext.get_instance().rmq_pub_client.get_rmq_pub_client),
):
    user = await ops_user.create_user(db, request)

    with rmq_pub_client:
        UserCreatedPublisher(rmq_pub_client).publish(
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
