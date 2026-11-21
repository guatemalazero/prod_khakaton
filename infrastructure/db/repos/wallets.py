from decimal import Decimal
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Wallet
from ....domain.dtos.user import WalletDTO


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_user_id(self, user_id: str) -> Optional[WalletDTO]:
        statement = select(Wallet).where(Wallet.user_id == user_id)
        result = await self._session.execute(statement)
        wallet = result.scalar_one_or_none()

        if wallet is None:
            return None

        return WalletDTO(
            user_id=wallet.user_id,
            balance=wallet.balance,
        )

    async def get_for_update(self, user_id: str) -> Optional[Wallet]:
        statement = (
            select(Wallet)
            .where(Wallet.user_id == user_id)
            .with_for_update()
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def update_balance(self, user_id: str, amount: Decimal) -> None:
        statement = (
            update(Wallet)
            .where(Wallet.user_id == user_id)
            .values(balance=Wallet.balance + amount)
        )
        await self._session.execute(statement)
        await self._session.flush()
