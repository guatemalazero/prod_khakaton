from datetime import datetime, timezone

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.group_purchase import GroupPurchaseDTO
from ....domain.enums import PurchaseStatus, ParticipantRole


class JoinGroupPurchaseUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        user_id: str,
        invite_code: str,
    ) -> GroupPurchaseDTO:
        group = await uow.group_purchases.get_by_invite_code(invite_code)
        if group is None:
            raise ValueError("Invalid invite code")

        if group.status != PurchaseStatus.ACTIVE:
            raise ValueError(f"Group purchase is {group.status}")

        now = datetime.now(timezone.utc)
        if group.expires_at <= now:
            raise ValueError("Group purchase has expired")

        if await uow.group_participants.exists(group.id, user_id):
            raise ValueError("User already in group")

        success = await uow.group_purchases.increment_joined_count(group.id)
        if not success:
            raise ValueError("Group purchase is full")

        await uow.group_participants.add(
            group_id=group.id,
            user_id=user_id,
            role=ParticipantRole.PARTICIPANT,
        )

        await uow.commit()
        return await uow.group_purchases.get_by_id(group.id)
