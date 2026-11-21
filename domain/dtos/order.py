from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ._base import BaseDataclass
from ..enums import OrderStatus


@dataclass
class OrderCreateDTO(BaseDataclass):
    idempotency_key: str
    product_id: str


@dataclass
class OrderDTO(BaseDataclass):
    id: str
    group_id: str
    user_id: str
    product_id: str
    fixed_price: Decimal
    status: OrderStatus
    idempotency_key: Optional[str]
    created_at: datetime
    paid_at: Optional[datetime]


@dataclass
class OrderListItemDTO(BaseDataclass):
    id: str
    group_id: str
    product_name: str
    fixed_price: Decimal
    status: OrderStatus
    created_at: datetime
    paid_at: Optional[datetime]
