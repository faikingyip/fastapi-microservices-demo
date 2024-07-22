from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db.db_base import DbBase
from src.constants.field_lengths import FieldLengths


class DbUser(DbBase):

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(FieldLengths.USER__EMAIL.value),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("email"),
        # Add more UniqueConstraint objects if needed
    )
