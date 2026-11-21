from ._base import UserUsecasesBase
from ....domain.dtos.user import AuthUserDTO
from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface


class RegisterUserUsecase(UserUsecasesBase):
    async def __call__(
        self,
        payload: AuthUserDTO,
        uow: UnitOfWorkInterface,
    ) -> str:
        await uow.users.create_user(payload.to_dict())

        session_string = self._func_service.create_session_string()

        self._redis_client.set(
            session_string,
            {"login": payload.login},
            10_000,
        )

        await uow.commit()
        return session_string