import decimal
from uuid import UUID

from sqlalchemy import Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.common.db.db_base import DbBase


class NegativeBalanceResultError(Exception):
    pass


class ChangeAmountZeroError(Exception):
    pass


class InconsistentVersionProposedError(Exception):
    pass


class Account(DbBase):

    __tablename__ = "account"

    user_id: Mapped[UUID] = mapped_column(nullable=False)

    balance: Mapped[decimal.Decimal] = mapped_column(
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

    def __repr__(self):
        return f"<Account {self.user_id=} {self.balance=} {self.version=}>"

    def __eq__(self, other):
        if not isinstance(other, Account):
            return False
        return other.user_id == self.user_id

    def __hash__(self):
        return hash(self.user_id)

    def update_balance(
        self,
        change_amount: decimal.Decimal,
        new_version: int,
    ):
        if change_amount == 0:
            raise ChangeAmountZeroError("The change amount cannot be 0.")

        if self.balance + change_amount < 0:
            raise NegativeBalanceResultError(
                (
                    f"The change amount {change_amount} "
                    "will result in a negative balance."
                )
            )

        if (self.version + 1) != new_version:
            raise InconsistentVersionProposedError(
                (
                    "The new version number must be greater than "
                    "the current version number by exactly 1."
                ),
            )

        self.version = new_version
        self.balance += change_amount
