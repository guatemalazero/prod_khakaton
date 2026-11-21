from fastapi import APIRouter

from ...deps import (
    uow,
    current_user_id,
    create_group_purchase as create_group_purchase_uc,
    get_group_purchase as get_group_purchase_uc,
    join_group_purchase as join_group_purchase_uc,
)
from ...domain.dtos.group_purchase import GroupPurchaseCreateDTO
from ..schemas import (
    GroupPurchaseCreateRequest,
    GroupPurchaseResponse,
    JoinGroupPurchaseRequest,
)

router = APIRouter(prefix='/group-purchases', tags=['Group Purchases'])


@router.post('/', response_model=GroupPurchaseResponse)
async def create_group_purchase(
    data: GroupPurchaseCreateRequest,
    user_id: current_user_id,
    uow: uow,
    create_group_purchase: create_group_purchase_uc,
) -> GroupPurchaseResponse:
    dto = GroupPurchaseCreateDTO(
        product_id=data.product_id,
        target_size=data.target_size,
        time_limit_minutes=data.time_limit_minutes,
    )
    group = await create_group_purchase(uow, user_id, dto)
    return GroupPurchaseResponse.model_validate(group)


@router.get('/{group_id}', response_model=GroupPurchaseResponse)
async def get_group_purchase(
    group_id: str,
    uow: uow,
    get_group_purchase: get_group_purchase_uc,
) -> GroupPurchaseResponse:
    group = await get_group_purchase(uow, group_id)
    return GroupPurchaseResponse.model_validate(group)


@router.post('/join', response_model=GroupPurchaseResponse)
async def join_group_purchase(
    data: JoinGroupPurchaseRequest,
    user_id: current_user_id,
    uow: uow,
    join_group_purchase: join_group_purchase_uc,
) -> GroupPurchaseResponse:
    group = await join_group_purchase(uow, user_id, data.invite_code)
    return GroupPurchaseResponse.model_validate(group)
