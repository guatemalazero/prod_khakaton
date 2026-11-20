from dataclasses import dataclass
from ._base import BaseDataclass


@dataclass()
class ItemDTO(BaseDataclass):
    id: str
    name: str
    price: int
    group_price: int
