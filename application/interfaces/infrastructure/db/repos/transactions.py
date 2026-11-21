from decimal import Decimal
from typing import Protocol, Optional, List

from ......domain.dtos.user import TransactionDTO
from ......domain.enums import TransactionType


class TransactionRepositoryInterface(Protocol):
    async def create(
        self,
        user_id: str,
        type: TransactionType,
        amount: Decimal,
        order_id: Optional[int] = None,
    ) -> str: ...

    async def exists_by_order_and_type(
        self,
        order_id: str,
        type: TransactionType,
    ) -> bool: ...

    async def list_by_user(self, user_id: str) -> List[TransactionDTO]: ...