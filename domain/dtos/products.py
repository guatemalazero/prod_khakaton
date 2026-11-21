from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List, Dict, Any

from ._base import BaseDataclass


@dataclass
class ProductDTO(BaseDataclass):
    id: str
    name: str
    regular_price: Decimal
    base_group_price: Decimal
    min_participants: int
    max_participants: int


@dataclass
class ProductDetailDTO(BaseDataclass):
    id: str
    name: str
    description: Optional[str]
    regular_price: Decimal
    base_group_price: Decimal
    pricing_rules: List[Dict[str, Any]]
    min_participants: int
    max_participants: int
    time_limit_minutes: int
    organizer_reward_percent: Decimal
