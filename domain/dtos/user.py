from dataclasses import dataclass
from ._base import BaseDataclass
from .group_buy import GroupBuyDTO

@dataclass()
class UserDTO(BaseDataclass):
    id: str
    login: str
    password: str

    group_buys: list[GroupBuyDTO]