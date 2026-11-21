from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ._base import BaseDataclass
from ..enums import OrderStatus


@dataclass
class OrderCreateDTO(BaseDataclass):
    """Входные данные для создания заказа."""
    idempotency_key: str
    product_id: int


@dataclass
class OrderDTO(BaseDataclass):
    """Ответ с информацией о заказе."""
    id: int
    group_id: int
    user_id: int
    product_id: int
    fixed_price: Decimal
    status: OrderStatus
    idempotency_key: Optional[str]
    created_at: datetime
    paid_at: Optional[datetime]


@dataclass
class OrderListItemDTO(BaseDataclass):
    """Упрощенный DTO для списков заказов."""
    id: int
    group_id: int
    product_name: str
    fixed_price: Decimal
    status: OrderStatus
    created_at: datetime
    paid_at: Optional[datetime]