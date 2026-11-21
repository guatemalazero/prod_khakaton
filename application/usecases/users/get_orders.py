from typing import List

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.order import OrderListItemDTO


class GetUserOrdersUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        user_id: str,
    ) -> List[OrderListItemDTO]:
        return await uow.orders.list_by_user(user_id)
