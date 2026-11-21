from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Item
from ....domain.dtos.items import ItemDTO


class ItemsRepo:
    def __init__(self, async_session: AsyncSession):
        self._session = async_session

    async def get_items(self) -> list[ItemDTO]:
        statement = select(Item)
        result = await self._session.execute(statement)
        items = result.scalars().all()

        return [
            ItemDTO(
                id=item.id,
                name=item.name,
                price=item.price,
                group_price=item.group_price,
            )
            for item in items
        ]

    async def get_item(self, item_id: str) -> Optional[ItemDTO]:
        statement = select(Item).where(Item.id == item_id)
        result = await self._session.execute(statement)
        item = result.scalar_one_or_none()

        if item is None:
            return None

        return ItemDTO(
            id=item.id,
            name=item.name,
            price=item.price,
            group_price=item.group_price,
        )
