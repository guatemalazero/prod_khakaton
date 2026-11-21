from typing import Optional

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.group_purchase import GroupPurchaseDTO


class GetGroupPurchaseUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        group_id: str,
    ) -> Optional[GroupPurchaseDTO]:
        return await uow.group_purchases.get_by_id(group_id)
