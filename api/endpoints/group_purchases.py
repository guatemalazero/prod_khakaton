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
async def _(
    data: GroupPurchaseCreateRequest,  # ← Pydantic на входе
    user_id: current_user_id,
    uow: uow,
    create_group_purchase: create_group_purchase_uc,
) -> GroupPurchaseResponse:
    
    # Pydantic → Dataclass перед передачей в usecase
    dto = GroupPurchaseCreateDTO(
        product_id=data.product_id,
        target_size=data.target_size,
        time_limit_minutes=data.time_limit_minutes,
    )
    
    group = await create_group_purchase(uow, user_id, dto)
    
    return GroupPurchaseResponse.model_validate(group)


@router.get('/{group_id}', response_model=GroupPurchaseResponse)
async def _(
    group_id: int,
    uow: uow,
    get_group_purchase: get_group_purchase_uc,
) -> GroupPurchaseResponse:
    
    group = await get_group_purchase(uow, group_id)
    
    return GroupPurchaseResponse.model_validate(group)


@router.post('/join', response_model=GroupPurchaseResponse)
async def _(
    data: JoinGroupPurchaseRequest,
    user_id: current_user_id,
    uow: uow,
    join_group_purchase: join_group_purchase_uc,
) -> GroupPurchaseResponse:
    
    group = await join_group_purchase(uow, user_id, data.invite_code)
    
    return GroupPurchaseResponse.model_validate(group)