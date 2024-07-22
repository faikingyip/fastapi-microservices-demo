from enum import Enum


class EventSubjects(str, Enum):
    """Defines the available event subjects that can be used."""

    TRANSACTION_CREATED = "transaction:created"
    ACCOUNT_UPDATED = "account:updated"
