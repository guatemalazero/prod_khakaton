from datetime import datetime
from decimal import Decimal
from typing import Optional

from ._base import BaseSchema


class WalletResponse(BaseSchema):
    user_id: str
    balance: Decimal


class TransactionResponse(BaseSchema):
    id: str
    user_id: str
    order_id: Optional[str]
    type: str
    amount: Decimal
    created_at: datetime


class OrderListItemResponse(BaseSchema):
    id: str
    group_id: str
    product_name: str
    fixed_price: Decimal
    status: str
    created_at: datetime
    paid_at: Optional[datetime]


class UserGroupPurchaseResponse(BaseSchema):
    id: str
    product_name: str
    status: str
    role: str
    current_joined_count: int
    target_size: int
    expires_at: datetime
    invite_code: Optional[str]