from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .repos.user import UsersRepo
from .repos.group_buy import GroupBuyRepo
from .repos.items import ItemsRepo


class UnitOfWork:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory

        self._async_session = None

    async def __aenter__(self) -> 'UnitOfWork':
        self._async_session = self._session_factory()

        self.users = UsersRepo(self._async_session)
        self.group_buy = GroupBuyRepo(self._async_session)
        self.items = ItemsRepo(self._async_session)

        return self

    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self._async_session.rollback()
        
        await self._async_session.close()

    async def commit(self) -> None:
        await self._async_session.commit()
