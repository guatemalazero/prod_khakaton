from ...interfaces.infrastructure.db.uow import UnitOfWorkInterface


class CreateGroupBuyUsecase:

    async def __call__(
        self,

        uow: UnitOfWorkInterface,
        item_id: str,
    ) -> str:

        group_buy_id = await uow.group_buy.create_group_buy(item_id)

        await uow.commit()

        return group_buy_id
