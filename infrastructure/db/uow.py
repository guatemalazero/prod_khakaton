from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class UnitOfWork:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory

        self._async_session = None

    async def __aenter__(self) -> 'UnitOfWork':
        self._async_session = self._session_factory()

        return self

    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self._async_session.rollback()
        
        await self._async_session.close()

    async def commit(self) -> None:
        await self._async_session.commit()
