from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from ._base import BaseSchema


class WalletResponse(BaseSchema):
    user_id: int
    balance: Decimal


class TransactionResponse(BaseSchema):
    id: int
    user_id: int
    order_id: Optional[int]
    type: str  # 'DEPOSIT' | 'PAYMENT' | 'REFUND' | 'REWARD'
    amount: Decimal
    created_at: datetime


class OrderListItemResponse(BaseSchema):
    id: int
    group_id: int
    product_name: str
    fixed_price: Decimal
    status: str
    created_at: datetime
    paid_at: Optional[datetime]


class UserGroupPurchaseResponse(BaseSchema):
    id: int
    product_name: str
    status: str
    role: str  # 'ORGANIZER' | 'PARTICIPANT'
    current_joined_count: int
    target_size: int
    expires_at: datetime
    invite_code: Optional[str]  # Только для организатора