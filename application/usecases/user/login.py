from ._base import UserUsecasesBase
from ....domain.dtos.user import AuthUserDTO
from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface


class LoginUserUsecase(UserUsecasesBase):
    async def __call__(
        self,
        payload: AuthUserDTO,
        uow: UnitOfWorkInterface,
    ) -> str | None:
        is_authenticated = await self._authenticate_user(payload, uow)

        if not is_authenticated:
            return None

        session_string = self._func_service.create_session_string()

        self._redis_client.set(
            session_string,
            {"login": payload.login},
            10_000,
        )

        return session_string