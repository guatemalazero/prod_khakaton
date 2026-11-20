from fastapi import APIRouter

from ...deps import uow
from ...domain.dtos.items import ItemDTO

router = APIRouter('/items')

@router.post('/get_items')
async def _(
    
    uow: uow
    # get_item: ...
) -> list[ItemDTO]:
    pass

@router.post('/get_item/{item_id}')
async def _(
    item_id: str,

    uow: uow,
    # get_item: ...
) -> ItemDTO:
    pass