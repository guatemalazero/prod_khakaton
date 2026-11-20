from fastapi import APIRouter
from ...deps import uow
from ...domain.dtos.group_buy import GroupBuyDTO

router = APIRouter('/group_buy')

@router.post('/{item_id}/create_group_buy')
async def _(
    item_id: str,

    uow: uow,
    # create_group_buy: ...
) -> str:
    pass

@router.get('/get/{group_buy_id}}')
async def _(
    group_buy_id: str,

    uow: uow,
    # get_group_buy: ...
) -> GroupBuyDTO :
    pass

@router.post('/add_user/{user_login}')
async def _(
    user_login: str,

    uow: uow,
    # add_user: ...
) -> ... :
    pass