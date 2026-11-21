from datetime import datetime
from decimal import Decimal
from typing import Protocol, Optional, List

from ......domain.dtos.group_purchase import GroupPurchaseDTO, UserGroupPurchaseDTO
from ......domain.enums import PurchaseStatus


class GroupPurchaseRepositoryInterface(Protocol):
    async def create(
        self,
        product_id: str,
        organizer_id: str,
        target_size: int,
        invite_code: str,
        expires_at: datetime,
    ) -> str: ...

    async def get_by_id(self, group_id: str) -> Optional[GroupPurchaseDTO]: ...

    async def get_by_invite_code(self, invite_code: str) -> Optional[GroupPurchaseDTO]: ...

    async def increment_joined_count(self, group_id: str) -> bool: ...

    async def increment_paid_count(self, group_id: str) -> bool: ...

    async def set_status(
        self,
        group_id: str,
        status: PurchaseStatus,
        completed_at: Optional[datetime] = None,
    ) -> None: ...

    async def list_by_user(self, user_id: str) -> List[UserGroupPurchaseDTO]: ...

    async def list_expired(self, now: datetime) -> List[int]: ...