from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.constants.field_lengths import FieldLengths
from src.db.models.db_base import DbBase


class DbUser(DbBase):

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(FieldLengths.EMAIL.value),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("email"),
        # Add more UniqueConstraint objects if needed
    )
