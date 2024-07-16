import json

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database import get_db
from src.common.rabbit_mq import get_rmq
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
    db: AsyncSession = Depends(get_db),
    rmq_cli=Depends(get_rmq),
):
    user = await ops_user.create_user(db, request)
    # msg = "First message published"
    # UserCreatedPublisher(rmq_cli).publish(msg)

    with rmq_cli:
        UserCreatedPublisher(rmq_cli).publish(
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
