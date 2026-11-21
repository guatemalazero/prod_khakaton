from datetime import datetime
from decimal import Decimal
from typing import Protocol, Optional, List

from ......domain.dtos.order import OrderDTO, OrderListItemDTO
from ......domain.enums import OrderStatus


class OrderRepositoryInterface(Protocol):
    async def create(
        self,
        group_id: str,
        user_id: str,
        product_id: str,
        fixed_price: Decimal,
        idempotency_key: Optional[str] = None,
    ) -> str: ...

    async def get_by_id(self, order_id: str) -> Optional[OrderDTO]: ...

    async def get_by_idempotency_key(self, idempotency_key: str) -> Optional[OrderDTO]: ...

    async def set_status(
        self,
        order_id: str,
        status: OrderStatus,
        paid_at: Optional[datetime] = None,
    ) -> None: ...

    async def list_by_user(self, user_id: str) -> List[OrderListItemDTO]: ...

    async def list_by_group(self, group_id: str) -> List[int]: ...