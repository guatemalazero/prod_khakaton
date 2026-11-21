from typing import Protocol, Optional
from decimal import Decimal

from ......domain.dtos.user import WalletDTO


class WalletRepositoryInterface(Protocol):
    async def get_by_user_id(self, user_id: str) -> Optional[WalletDTO]: ...
    async def update_balance(self, user_id: str, amount: Decimal) -> None: ...