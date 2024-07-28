from dataclasses import dataclass
from datetime import date
from typing import Optional


class Event:
    pass


@dataclass
class UserSignupRequested(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None


@dataclass
class UserSigninRequested(Event):
    ref: str
    sku: str
    qty: int
    eta: Optional[date] = None
