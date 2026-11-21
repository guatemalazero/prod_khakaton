from typing import Protocol, Optional

from ......domain.dtos.items import ItemDTO


class ItemsRepoInterface(Protocol):
    async def get_items(self) -> list[ItemDTO]: ...
    async def get_item(self, item_id: str) -> Optional[ItemDTO]: ...
