from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field

from ._base import BaseSchema


class OrderCreateRequest(BaseSchema):
    idempotency_key: str = Field(..., min_length=1, max_length=64, description="Ключ идемпотентности")
    product_id: str


class OrderResponse(BaseSchema):
    id: str
    group_id: str
    user_id: str
    product_id: str
    fixed_price: Decimal
    status: str
    idempotency_key: Optional[str]
    created_at: datetime
    paid_at: Optional[datetime]