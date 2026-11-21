from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Order, Product
from ....domain.dtos.order import OrderDTO, OrderListItemDTO
from ....domain.enums import OrderStatus


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        group_id: str,
        user_id: str,
        product_id: str,
        fixed_price: Decimal,
        idempotency_key: Optional[str] = None,
    ) -> str:
        order = Order(
            group_id=group_id,
            user_id=user_id,
            product_id=product_id,
            fixed_price=fixed_price,
            idempotency_key=idempotency_key,
        )
        self._session.add(order)
        await self._session.flush()
        return order.id

    async def get_by_id(self, order_id: str) -> Optional[OrderDTO]:
        statement = select(Order).where(Order.id == order_id)
        result = await self._session.execute(statement)
        order = result.scalar_one_or_none()

        if order is None:
            return None

        return OrderDTO(
            id=order.id,
            group_id=order.group_id,
            user_id=order.user_id,
            product_id=order.product_id,
            fixed_price=order.fixed_price,
            status=order.status,
            idempotency_key=order.idempotency_key,
            created_at=order.created_at,
            paid_at=order.paid_at,
        )

    async def get_by_idempotency_key(self, idempotency_key: str) -> Optional[OrderDTO]:
        statement = select(Order).where(Order.idempotency_key == idempotency_key)
        result = await self._session.execute(statement)
        order = result.scalar_one_or_none()

        if order is None:
            return None

        return OrderDTO(
            id=order.id,
            group_id=order.group_id,
            user_id=order.user_id,
            product_id=order.product_id,
            fixed_price=order.fixed_price,
            status=order.status,
            idempotency_key=order.idempotency_key,
            created_at=order.created_at,
            paid_at=order.paid_at,
        )

    async def get_for_update(self, order_id: str) -> Optional[Order]:
        """Блокировка строки заказа."""
        statement = (
            select(Order)
            .where(Order.id == order_id)
            .with_for_update()
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def set_status(
        self,
        order_id: str,
        status: OrderStatus,
        paid_at: Optional[datetime] = None,
    ) -> None:
        statement = (
            select(Order)
            .where(Order.id == order_id)
            .with_for_update()
        )
        result = await self._session.execute(statement)
        order = result.scalar_one_or_none()

        if order:
            order.status = status
            if paid_at:
                order.paid_at = paid_at
            await self._session.flush()

    async def list_by_user(self, user_id: str) -> List[OrderListItemDTO]:
        statement = (
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        result = await self._session.execute(statement)
        orders = result.scalars().all()

        product_ids = [o.product_id for o in orders]
        products_stmt = select(Product).where(Product.id.in_(product_ids))
        products_result = await self._session.execute(products_stmt)
        products_map = {p.id: p.name for p in products_result}

        return [
            OrderListItemDTO(
                id=o.id,
                group_id=o.group_id,
                product_name=products_map.get(o.product_id, "Unknown"),
                fixed_price=o.fixed_price,
                status=o.status,
                created_at=o.created_at,
                paid_at=o.paid_at,
            )
            for o in orders
        ]

    async def list_by_group(self, group_id: str) -> List[Order]:
        """Все заказы в закупке (для массового возврата при отмене)."""
        statement = select(Order).where(Order.group_id == group_id)
        result = await self._session.execute(statement)
        return result.scalars().all()