from fastapi import APIRouter

from ...deps import (
    uow,
    current_user_id,
    create_order as create_order_uc,
    pay_order as pay_order_uc,
)
from ...domain.dtos.order import OrderCreateDTO
from ..schemas import OrderCreateRequest, OrderResponse

router = APIRouter(prefix='/orders', tags=['Orders'])


@router.post('/{group_id}', response_model=OrderResponse)
async def create_order(
    group_id: str,
    data: OrderCreateRequest,
    user_id: current_user_id,
    uow: uow,
    create_order: create_order_uc,
) -> OrderResponse:
    dto = OrderCreateDTO(
        idempotency_key=data.idempotency_key,
        product_id=data.product_id,
    )
    order = await create_order(uow, user_id, group_id, dto)
    return OrderResponse.model_validate(order)


@router.post('/{order_id}/pay', status_code=204)
async def pay_order(
    order_id: str,
    uow: uow,
    pay_order: pay_order_uc,
) -> None:
    await pay_order(uow, order_id)
