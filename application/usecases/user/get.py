from ...interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.user import UserDTO


class GetUserUsecase:

    async def __call__(
        self,

        uow: UnitOfWorkInterface ,
        login: str
    ) -> UserDTO:

        user = await uow.users.get_user(login)

        return user