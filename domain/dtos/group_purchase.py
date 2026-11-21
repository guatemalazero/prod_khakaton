from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from ._base import BaseDataclass
from ..enums import PurchaseStatus, ParticipantRole


@dataclass
class GroupPurchaseCreateDTO(BaseDataclass):
    product_id: str
    target_size: int
    time_limit_minutes: int


@dataclass
class GroupPurchaseDTO(BaseDataclass):
    id: str
    product_id: str
    organizer_id: str
    status: PurchaseStatus
    target_size: int
    current_joined_count: int
    current_paid_count: int
    invite_code: str
    created_at: datetime
    expires_at: datetime
    completed_at: Optional[datetime]
    current_calculated_price: Decimal


@dataclass
class GroupPurchaseListItemDTO(BaseDataclass):
    id: str
    product_name: str
    status: PurchaseStatus
    current_joined_count: int
    target_size: int
    expires_at: datetime


@dataclass
class UserGroupPurchaseDTO(BaseDataclass):
    id: str
    product_name: str
    status: PurchaseStatus
    role: ParticipantRole
    current_joined_count: int
    target_size: int
    expires_at: datetime
    invite_code: Optional[str]
