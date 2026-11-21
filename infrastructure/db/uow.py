from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .repos.group_participants import GroupParticipantRepository
from .repos.group_purchases import GroupPurchaseRepository
from .repos.orders import OrderRepository
from .repos.products import ProductRepository
from .repos.transactions import TransactionRepository
from .repos.users import UserRepository
from .repos.wallets import WalletRepository


class UnitOfWork:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory

        self._async_session = None

    async def __aenter__(self) -> 'UnitOfWork':
        self._async_session = self._session_factory()

        self.users = UserRepository(self._async_session)
        self.wallets = WalletRepository(self._async_session)
        self.products = ProductRepository(self._async_session)
        self.group_purchases = GroupPurchaseRepository(self._async_session)
        self.group_participants = GroupParticipantRepository(self._async_session)
        self.orders = OrderRepository(self._async_session)
        self.transactions = TransactionRepository(self._async_session)

        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self._async_session.rollback()

        await self._async_session.close()

    async def commit(self) -> None:
        await self._async_session.commit()

    async def rollback(self) -> None:
        await self._async_session.rollback()