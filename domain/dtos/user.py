from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ._base import BaseDataclass
from ..enums import TransactionType


@dataclass
class WalletDTO(BaseDataclass):
    """Информация о кошельке пользователя."""
    user_id: int
    balance: Decimal


@dataclass
class TransactionDTO(BaseDataclass):
    """Информация о транзакции."""
    id: int
    user_id: int
    order_id: Optional[int]
    type: TransactionType
    amount: Decimal
    created_at: datetime


@dataclass
class UserDTO(BaseDataclass):
    """Базовая информация о пользователе."""
    id: int
    name: str
    created_at: datetime