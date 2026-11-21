from typing import Protocol
from .repos.user import UsersRepoInteface
from .repos.group_buy import GroupBuyRepoInterface
from .repos.items import ItemsRepoInterface

class UnitOfWorkInterface(Protocol):
    users: UsersRepoInteface
    group_buy: GroupBuyRepoInterface
    items: ItemsRepoInterface

    async def commit(self) -> None: ...