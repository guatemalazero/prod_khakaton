from typing import Protocol

from .repos.users import UserRepositoryInterface
from .repos.wallets import WalletRepositoryInterface
from .repos.products import ProductRepositoryInterface
from .repos.group_purchases import GroupPurchaseRepositoryInterface
from .repos.group_participants import GroupParticipantRepositoryInterface
from .repos.orders import OrderRepositoryInterface
from .repos.transactions import TransactionRepositoryInterface


class UnitOfWorkInterface(Protocol):
    # Репозитории
    users: UserRepositoryInterface
    wallets: WalletRepositoryInterface
    products: ProductRepositoryInterface
    group_purchases: GroupPurchaseRepositoryInterface
    group_participants: GroupParticipantRepositoryInterface
    orders: OrderRepositoryInterface
    transactions: TransactionRepositoryInterface

    # Управление транзакцией
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...