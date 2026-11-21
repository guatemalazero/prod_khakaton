from datetime import datetime, timezone

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.order import OrderCreateDTO, OrderDTO
from ....domain.enums import PurchaseStatus


class CreateOrderUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        user_id: str,
        group_id: str,
        data: OrderCreateDTO,
    ) -> OrderDTO:
        if data.idempotency_key:
            existing_order = await uow.orders.get_by_idempotency_key(data.idempotency_key)
            if existing_order is not None:
                return existing_order

        group = await uow.group_purchases.get_by_id(group_id)
        if group is None:
            raise ValueError(f"Group purchase {group_id} not found")

        if group.status != PurchaseStatus.ACTIVE:
            raise ValueError(f"Group purchase is {group.status}, cannot create order")

        now = datetime.now(timezone.utc)
        if group.expires_at <= now:
            raise ValueError("Group purchase has expired")

        if not await uow.group_participants.exists(group_id, user_id):
            raise ValueError("User is not a participant of this group purchase")

        existing_user_order = await uow.orders.get_by_group_and_user(group_id, user_id)
        if existing_user_order is not None:
            raise ValueError("User already has an order in this group purchase")

        if group.product_id != data.product_id:
            raise ValueError("Product does not match the group purchase product")

        fixed_price = group.current_calculated_price

        order_id = await uow.orders.create(
            group_id=group_id,
            user_id=user_id,
            product_id=data.product_id,
            fixed_price=fixed_price,
            idempotency_key=data.idempotency_key,
        )

        await uow.commit()
        return await uow.orders.get_by_id(order_id)
