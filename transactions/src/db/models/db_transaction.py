from decimal import Decimal
from uuid import UUID

from sqlalchemy import Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.db_base import DbBase


class DbTransaction(DbBase):

    __tablename__ = "transaction"

    user_id: Mapped[UUID] = mapped_column(nullable=False, index=True)

    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )

    last_trans_id: Mapped[UUID] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("last_trans_id"),
        # Add more UniqueConstraint objects if needed
    )
