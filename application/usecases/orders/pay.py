from datetime import datetime, timezone
from decimal import Decimal

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.order import OrderDTO
from ....domain.enums import OrderStatus, TransactionType, PurchaseStatus


class PayOrderUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        order_id: str,
    ) -> OrderDTO:
        order = await uow.orders.get_for_update(order_id)
        if order is None:
            raise ValueError(f"Order {order_id} not found")

        if order.status != OrderStatus.PENDING:
            raise ValueError(f"Order is {order.status}, cannot pay")

        if await uow.transactions.exists_by_order_and_type(
            order_id=order_id,
            type=TransactionType.PAYMENT,
        ):
            return await uow.orders.get_by_id(order_id)

        wallet = await uow.wallets.get_for_update(order.user_id)
        if wallet is None:
            raise ValueError("Wallet not found")

        if wallet.balance < order.fixed_price:
            raise ValueError(
                f"Insufficient funds: balance={wallet.balance}, "
                f"required={order.fixed_price}"
            )

        await uow.wallets.update_balance(
            user_id=order.user_id,
            amount=-order.fixed_price,
        )

        await uow.transactions.create(
            user_id=order.user_id,
            order_id=order_id,
            type=TransactionType.PAYMENT,
            amount=order.fixed_price,
        )

        now = datetime.now(timezone.utc)
        await uow.orders.set_status(
            order_id=order_id,
            status=OrderStatus.PAID,
            paid_at=now,
        )

        success = await uow.group_purchases.increment_paid_count(order.group_id)
        if not success:
            raise ValueError("Failed to increment paid count")

        group = await uow.group_purchases.get_by_id(order.group_id)
        if group.current_paid_count >= group.target_size:
            await uow.group_purchases.set_status(
                group_id=order.group_id,
                status=PurchaseStatus.SUCCESS,
                completed_at=now,
            )
            await self._reward_organizer(uow, order.group_id, group.organizer_id)

        await uow.commit()
        return await uow.orders.get_by_id(order_id)

    async def _reward_organizer(
        self,
        uow: UnitOfWorkInterface,
        group_id: str,
        organizer_id: str,
    ) -> None:
        paid_orders = await uow.orders.list_by_group(
            group_id=group_id,
            status=OrderStatus.PAID,
        )

        total_amount = sum(order.fixed_price for order in paid_orders)

        group = await uow.group_purchases.get_by_id(group_id)
        product = await uow.products.get_by_id(group.product_id)

        if product is None:
            return

        reward_percent = product.organizer_reward_percent
        reward_amount = (total_amount * reward_percent / Decimal("100")).quantize(
            Decimal("0.01")
        )

        if reward_amount <= 0:
            return

        if paid_orders:
            first_order_id = paid_orders[0].id
            if await uow.transactions.exists_by_order_and_type(
                order_id=first_order_id,
                type=TransactionType.REWARD,
            ):
                return

        await uow.wallets.update_balance(
            user_id=organizer_id,
            amount=reward_amount,
        )

        await uow.transactions.create(
            user_id=organizer_id,
            order_id=paid_orders[0].id if paid_orders else None,
            type=TransactionType.REWARD,
            amount=reward_amount,
        )
