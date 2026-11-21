from typing import List

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.group_purchase import UserGroupPurchaseDTO


class GetUserGroupPurchaseUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        user_id: str,
    ) -> List[UserGroupPurchaseDTO]:
        return await uow.group_purchases.list_by_user(user_id)
