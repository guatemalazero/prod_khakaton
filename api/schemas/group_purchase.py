from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import Field

from ._base import BaseSchema


class GroupPurchaseCreateRequest(BaseSchema):
    """Запрос на создание закупки."""
    product_id: int
    target_size: int = Field(..., ge=2, le=100, description="Сколько участников нужно")
    time_limit_minutes: int = Field(..., ge=1, le=1440, description="Лимит времени в минутах")


class GroupPurchaseResponse(BaseSchema):
    """Ответ с информацией о закупке."""
    id: int
    product_id: int
    organizer_id: int
    status: str  # 'ACTIVE' | 'SUCCESS' | 'CANCELED'
    target_size: int
    current_joined_count: int
    current_paid_count: int
    invite_code: str
    created_at: datetime
    expires_at: datetime
    completed_at: Optional[datetime]
    current_calculated_price: Decimal


class JoinGroupPurchaseRequest(BaseSchema):
    """Запрос на вступление в закупку."""
    invite_code: str = Field(..., min_length=1, max_length=32)