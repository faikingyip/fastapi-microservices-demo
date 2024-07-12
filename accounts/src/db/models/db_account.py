from decimal import Decimal
from uuid import UUID

from sqlalchemy import Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.db.models.db_base import DbBase


class DbAccount(DbBase):

    __tablename__ = "account"

    user_id: Mapped[UUID] = mapped_column(nullable=False)

    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )

    last_trans_id: Mapped[UUID] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id"),
        # Add more UniqueConstraint objects if needed
    )
