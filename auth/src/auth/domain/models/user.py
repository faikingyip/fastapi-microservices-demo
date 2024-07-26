from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db.db_base import DbBase
from src.constants.field_lengths import FieldLengths
from src.utils import hash as h


class User(DbBase):

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

    def __repr__(self):
        return (
            f"<User {self.id=} {self.email=} "
            f"{self.first_name=} {self.last_name=} "
            f"{self.created_on=} {self.last_updated_on=} >"
        )

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.id == self.id

    def __hash__(self):
        return hash(self.id)

    def is_password_valid(self, password) -> bool:
        return h.verify_bcrypt(
            password,
            self.password_hash,
        )

    # def update_balance(
    #     self,
    #     change_amount: decimal.Decimal,
    #     new_version: int,
    # ):
    #     if change_amount == 0:
    #         raise ChangeAmountZeroError("The change amount cannot be 0.")

    #     if self.balance + change_amount < 0:
    #         raise NegativeBalanceResultError(
    #             f"The change amount {change_amount} ",
    #             "will result in a negative balance.",
    #         )

    #     if (self.version + 1) != new_version:
    #         raise InconsistentVersionProposedError(
    #             (
    #                 "The new version number must be greater than ",
    #                 "the current version number by exactly 1.",
    #             ),
    #         )

    #     self.version = new_version
    #     self.balance += change_amount
