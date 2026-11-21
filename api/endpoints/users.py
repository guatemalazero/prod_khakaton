from typing import List

from fastapi import APIRouter

from ...deps import (
    uow,
    current_user_id,
    get_user_wallet as get_user_wallet_uc,
    get_user_transactions as get_user_transactions_uc,
    get_user_orders as get_user_orders_uc,
    get_user_group_purchases as get_user_group_purchases_uc,
)
from ..schemas import (
    WalletResponse,
    TransactionResponse,
    OrderListItemResponse,
    UserGroupPurchaseResponse,
)

router = APIRouter(prefix='/users/me', tags=['User Cabinet'])


@router.get('/wallet', response_model=WalletResponse)
async def _(
    user_id: current_user_id,
    uow: uow,
    get_user_wallet: get_user_wallet_uc,
) -> WalletResponse:
    
    wallet = await get_user_wallet(uow, user_id)
    
    return WalletResponse.model_validate(wallet)


@router.get('/transactions', response_model=List[TransactionResponse])
async def _(
    user_id: current_user_id,
    uow: uow,
    get_user_transactions: get_user_transactions_uc,
) -> List[TransactionResponse]:
    
    transactions = await get_user_transactions(uow, user_id)
    
    return [TransactionResponse.model_validate(t) for t in transactions]


@router.get('/orders', response_model=List[OrderListItemResponse])
async def _(
    user_id: current_user_id,
    uow: uow,
    get_user_orders: get_user_orders_uc,
) -> List[OrderListItemResponse]:
    
    orders = await get_user_orders(uow, user_id)
    
    return [OrderListItemResponse.model_validate(o) for o in orders]


@router.get('/group-purchases', response_model=List[UserGroupPurchaseResponse])
async def _(
    user_id: current_user_id,
    uow: uow,
    get_user_group_purchases: get_user_group_purchases_uc,
) -> List[UserGroupPurchaseResponse]:
    
    purchases = await get_user_group_purchases(uow, user_id)
    
    return [UserGroupPurchaseResponse.model_validate(p) for p in purchases]