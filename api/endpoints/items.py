from fastapi import APIRouter

from ...deps import (
    uow,
    get_item as get_item_uc,
    get_items as get_items_uc,
)
from ...domain.dtos.items import ItemDTO

router = APIRouter(prefix='/items')

@router.post('/get_items')
async def _(

    uow: uow,
    get_items: get_items_uc,
) -> list[ItemDTO]:

    items = await get_items(uow)

    return items

@router.post('/get_item/{item_id}')
async def _(
    item_id: str,

    uow: uow,
    get_item: get_item_uc,
) -> ItemDTO:

    item = await get_item(uow, item_id)

    return item
