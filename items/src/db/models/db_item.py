from decimal import Decimal

from sqlalchemy import Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.constants.field_lengths import FieldLengths
from src.db.models.db_base import DbBase


class DbItem(DbBase):

    __tablename__ = "item"

    title: Mapped[str] = mapped_column(
        String(FieldLengths.ITEM__TITLE.value),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(FieldLengths.ITEM__DESC.value),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("title"),
        # Add more UniqueConstraint objects if needed
    )
