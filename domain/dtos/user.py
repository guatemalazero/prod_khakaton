from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ._base import BaseDataclass
from ..enums import TransactionType


@dataclass
class WalletDTO(BaseDataclass):
    user_id: str
    balance: Decimal


@dataclass
class TransactionDTO(BaseDataclass):
    id: str
    user_id: str
    order_id: Optional[str]
    type: TransactionType
    amount: Decimal
    created_at: datetime


@dataclass
class UserDTO(BaseDataclass):
    id: str
    name: str
    created_at: datetime
