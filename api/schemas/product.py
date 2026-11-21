from decimal import Decimal
from typing import Optional, List

from pydantic import Field

from ._base import BaseSchema


class PricingRuleResponse(BaseSchema):
    min_participants: int
    price: Decimal


class ProductResponse(BaseSchema):
    id: str
    name: str
    regular_price: Decimal
    base_group_price: Decimal
    min_participants: int
    max_participants: int


class ProductDetailResponse(BaseSchema):
    id: str
    name: str
    description: Optional[str]
    regular_price: Decimal
    base_group_price: Decimal
    pricing_rules: List[PricingRuleResponse]
    min_participants: int
    max_participants: int
    time_limit_minutes: int
    organizer_reward_percent: Decimal