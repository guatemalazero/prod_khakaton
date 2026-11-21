from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface


class TestPaymentUsecase:

    async def __call__(
        self,

        group_buy_id: str,
        uow: UnitOfWorkInterface
    ) -> None:
        await uow.group_buy.test_payment(group_buy_id=group_buy_id)

        