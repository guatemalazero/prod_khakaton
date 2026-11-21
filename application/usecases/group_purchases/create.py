import secrets
from datetime import datetime, timedelta, timezone

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.group_purchase import GroupPurchaseCreateDTO, GroupPurchaseDTO
from ....domain.enums import ParticipantRole


class CreateGroupPurchaseUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        user_id: str,
        data: GroupPurchaseCreateDTO,
    ) -> GroupPurchaseDTO:
        product = await uow.products.get_by_id(data.product_id)
        if product is None:
            raise ValueError(f"Product {data.product_id} not found")

        if not (product.min_participants <= data.target_size <= product.max_participants):
            raise ValueError(
                f"target_size must be between {product.min_participants} "
                f"and {product.max_participants}"
            )

        invite_code = secrets.token_urlsafe(16)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=data.time_limit_minutes)

        group_id = await uow.group_purchases.create(
            product_id=data.product_id,
            organizer_id=user_id,
            target_size=data.target_size,
            invite_code=invite_code,
            expires_at=expires_at,
        )

        await uow.group_participants.add(
            group_id=group_id,
            user_id=user_id,
            role=ParticipantRole.ORGANIZER,
        )

        await uow.commit()
        return await uow.group_purchases.get_by_id(group_id)
