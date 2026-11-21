from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field

from ._base import BaseSchema


class OrderCreateRequest(BaseSchema):
    """Запрос на создание заказа."""
    idempotency_key: str = Field(..., min_length=1, max_length=64)
    product_id: int


class OrderResponse(BaseSchema):
    """Ответ с информацией о заказе."""
    id: int
    group_id: int
    user_id: int
    product_id: int
    fixed_price: Decimal
    status: str  # 'PENDING' | 'PAID' | 'REFUNDED'
    idempotency_key: Optional[str]
    created_at: datetime
    paid_at: Optional[datetime]