from decimal import Decimal
from uuid import UUID

from sqlalchemy import Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.db_base import DbBase


class DbTransaction(DbBase):

    __tablename__ = "transaction"

    user_id: Mapped[UUID] = mapped_column(nullable=False, index=True)

    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )

    version: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "version",
            name="uix_user_version",
        ),
    )
