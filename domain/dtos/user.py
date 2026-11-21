from dataclasses import dataclass
from ._base import BaseDataclass
from .group_buy import GroupBuyDTO
from ..enums import UserRole

@dataclass()
class AuthUserDTO(BaseDataclass):
    login: str
    password: str

@dataclass()
class UserDTO(BaseDataclass):
    id: str
    login: str
    password: str
    role: UserRole

    group_buys: list[GroupBuyDTO]

@dataclass()
class UpdateUserDTO(BaseDataclass):
    login: str
    password: str
    role: UserRole
