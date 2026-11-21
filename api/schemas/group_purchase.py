from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field

from ._base import BaseSchema


class GroupPurchaseCreateRequest(BaseSchema):
    product_id: str
    target_size: int = Field(..., ge=2, le=100, description="Сколько участников нужно")
    time_limit_minutes: int = Field(..., ge=1, le=1440, description="Лимит времени в минутах")


class GroupPurchaseResponse(BaseSchema):
    id: str
    product_id: str
    organizer_id: str
    status: str
    target_size: int
    current_joined_count: int
    current_paid_count: int
    invite_code: str
    created_at: datetime
    expires_at: datetime
    completed_at: Optional[datetime]
    current_calculated_price: Decimal


class JoinGroupPurchaseRequest(BaseSchema):
    invite_code: str = Field(..., min_length=1, max_length=32, description="Код приглашения")