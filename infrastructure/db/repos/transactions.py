from decimal import Decimal
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Transaction
from ....domain.dtos.user import TransactionDTO
from ....domain.enums import TransactionType


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        user_id: str,
        type: TransactionType,
        amount: Decimal,
        order_id: Optional[int] = None,
    ) -> str:
        transaction = Transaction(
            user_id=user_id,
            order_id=order_id,
            type=type,
            amount=amount,
        )
        self._session.add(transaction)
        await self._session.flush()
        return transaction.id

    async def exists_by_order_and_type(
        self,
        order_id: str,
        type: TransactionType,
    ) -> bool:
        """Проверка идемпотентности (чтобы не было повторных возвратов)."""
        statement = select(Transaction).where(
            Transaction.order_id == order_id,
            Transaction.type == type,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none() is not None

    async def list_by_user(self, user_id: str) -> List[TransactionDTO]:
        statement = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
        )
        result = await self._session.execute(statement)
        transactions = result.scalars().all()

        return [
            TransactionDTO(
                id=t.id,
                user_id=t.user_id,
                order_id=t.order_id,
                type=t.type,
                amount=t.amount,
                created_at=t.created_at,
            )
            for t in transactions
        ]