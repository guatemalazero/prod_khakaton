from ...interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.group_buy import GroupBuyDTO


class GetGroupBuyUsecase:

    async def __call__(
        self,

        uow: UnitOfWorkInterface,
        group_buy_id: str,
    ) -> GroupBuyDTO | None:

        group_buy = await uow.group_buy.get_group_buy(group_buy_id)

        return group_buy
