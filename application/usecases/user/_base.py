from ...interfaces.infrastructure.redis_client import RedisClientInterface
from ....application.interfaces.services.func import FuncServiceInterface
from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.user import AuthUserDTO


class UserUsecasesBase:
    def __init__(
        self,
        redis_client: RedisClientInterface,
        func_service: FuncServiceInterface,
    ):
        self._redis_client = redis_client
        self._func_service = func_service

    async def _authenticate_user(
        self,
        payload: AuthUserDTO,
        uow: UnitOfWorkInterface,
    ) -> bool:
        user = await uow.users.get_user(payload.login)

        if user is None:
            return False

        # В реальном проекте здесь должно быть сравнение хешей
        return user.password == payload.password