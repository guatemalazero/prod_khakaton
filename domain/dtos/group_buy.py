from dataclasses import dataclass
from ._base import BaseDataclass
from ..enums import GroupBuyStatus


@dataclass()
class GroupBuyDTO(BaseDataclass):
    id: str
    status: GroupBuyStatus
    current_people_count: int
    current_money_count: str

    item_id: str
    url: str
    expire: int

@dataclass()
class GroupBuyTermsDTO(BaseDataclass):
    id: str
    people_count: int

cl = GroupBuyDTO()