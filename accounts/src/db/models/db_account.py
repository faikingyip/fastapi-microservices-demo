from decimal import Decimal
from uuid import UUID

from sqlalchemy import Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db.db_base import DbBase


class DbAccount(DbBase):

    __tablename__ = "account"

    user_id: Mapped[UUID] = mapped_column(nullable=False)

    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )

    version: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id"),
        UniqueConstraint(
            "user_id",
            "version",
        ),
        # Add more UniqueConstraint objects if needed
    )
