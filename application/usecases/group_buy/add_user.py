from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface

class AddUserUsecase:

    async def __call__(
        self,

        user_login: str,
        group_buy_id: str,
        uow: UnitOfWorkInterface
    ):
        await uow.group_buy.add_user(group_buy_id, user_login)
        await uow.commit()
        