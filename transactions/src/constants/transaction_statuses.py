from enum import Enum


class TransactionStatuses(Enum):
    PENDING = 1
    COMPLETED = 2
    DECLINED = 3
