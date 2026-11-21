from typing import Optional

from fastapi import APIRouter
from ...deps import (
    uow,
    create_group_buy as create_group_buy_uc,
    get_group_buy as get_group_buy_uc,
    add_user as add_user_uc,
    test_payment as test_payment_uc
)
from ...domain.dtos.group_buy import GroupBuyDTO

router = APIRouter(prefix='/group_buy')

@router.post('/{item_id}/create_group_buy')
async def _(
    item_id: str,

    uow: uow,
    create_group_buy: create_group_buy_uc,
) -> str:

    group_buy_id = await create_group_buy(uow, item_id)

    return group_buy_id

@router.get('/get/{group_buy_id}')
async def _(
    group_buy_id: str,

    uow: uow,
    get_group_buy: get_group_buy_uc,
) -> Optional[GroupBuyDTO]:

    group_buy = await get_group_buy(uow, group_buy_id)

    return group_buy

@router.post('{group_buy_id}/add_user/{user_login}')
async def _(
    group_buy_id: str,
    user_login: str,

    uow: uow,
    add_user: add_user_uc
) -> None :
    await add_user(user_login, group_buy_id, uow)

@router.post('/test_payment/{group_buy_id}')
async def _(
    group_buy_id: int,

    uow: uow,
    test_payment: test_payment_uc
) -> None :
    await test_payment(group_buy_id, uow)