from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import GroupPurchase, GroupParticipant, Product
from ....domain.dtos.group_purchase import GroupPurchaseDTO, UserGroupPurchaseDTO
from ....domain.enums import PurchaseStatus


class GroupPurchaseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        product_id: str,
        organizer_id: str,
        target_size: int,
        invite_code: str,
        expires_at: datetime,
    ) -> str:
        group = GroupPurchase(
            product_id=product_id,
            organizer_id=organizer_id,
            target_size=target_size,
            invite_code=invite_code,
            expires_at=expires_at,
        )
        self._session.add(group)
        await self._session.flush()
        return group.id

    async def get_by_id(self, group_id: str) -> Optional[GroupPurchaseDTO]:
        statement = (
            select(GroupPurchase)
            .where(GroupPurchase.id == group_id)
        )
        result = await self._session.execute(statement)
        group = result.scalar_one_or_none()

        if group is None:
            return None

        current_price = await self._calculate_current_price(group)

        return GroupPurchaseDTO(
            id=group.id,
            product_id=group.product_id,
            organizer_id=group.organizer_id,
            status=group.status,
            target_size=group.target_size,
            current_joined_count=group.current_joined_count,
            current_paid_count=group.current_paid_count,
            invite_code=group.invite_code,
            created_at=group.created_at,
            expires_at=group.expires_at,
            completed_at=group.completed_at,
            current_calculated_price=current_price,
        )

    async def _calculate_current_price(self, group: GroupPurchase) -> Decimal:
        """Расчёт текущей цены на основе pricing_rules и current_joined_count."""
        stmt = select(Product).where(Product.id == group.product_id)
        result = await self._session.execute(stmt)
        product = result.scalar_one()

        rules = product.pricing_rules or []
        applicable_rules = [r for r in rules if r.get('min_participants', 0) <= group.current_joined_count]
        
        if applicable_rules:
            best_rule = max(applicable_rules, key=lambda r: r.get('min_participants', 0))
            return Decimal(str(best_rule.get('price', product.base_group_price)))
        
        return product.base_group_price

    async def get_by_invite_code(self, invite_code: str) -> Optional[GroupPurchaseDTO]:
        statement = select(GroupPurchase).where(GroupPurchase.invite_code == invite_code)
        result = await self._session.execute(statement)
        group = result.scalar_one_or_none()

        if group is None:
            return None

        current_price = await self._calculate_current_price(group)

        return GroupPurchaseDTO(
            id=group.id,
            product_id=group.product_id,
            organizer_id=group.organizer_id,
            status=group.status,
            target_size=group.target_size,
            current_joined_count=group.current_joined_count,
            current_paid_count=group.current_paid_count,
            invite_code=group.invite_code,
            created_at=group.created_at,
            expires_at=group.expires_at,
            completed_at=group.completed_at,
            current_calculated_price=current_price,
        )

    async def get_for_update(self, group_id: str) -> Optional[GroupPurchase]:
        """Блокировка строки закупки для конкурентных операций."""
        statement = (
            select(GroupPurchase)
            .where(GroupPurchase.id == group_id)
            .with_for_update()
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def increment_joined_count(self, group_id: str) -> bool:
        """Атомарный инкремент с защитой от переполнения."""
        statement = (
            update(GroupPurchase)
            .where(
                GroupPurchase.id == group_id,
                GroupPurchase.status == PurchaseStatus.ACTIVE,
                GroupPurchase.current_joined_count < GroupPurchase.target_size,
            )
            .values(current_joined_count=GroupPurchase.current_joined_count + 1)
            .returning(GroupPurchase.id)
        )
        result = await self._session.execute(statement)
        await self._session.flush()
        return result.scalar_one_or_none() is not None

    async def increment_paid_count(self, group_id: str) -> bool:
        """Атомарный инкремент оплаченных."""
        statement = (
            update(GroupPurchase)
            .where(
                GroupPurchase.id == group_id,
                GroupPurchase.current_paid_count < GroupPurchase.target_size,
            )
            .values(current_paid_count=GroupPurchase.current_paid_count + 1)
            .returning(GroupPurchase.id)
        )
        result = await self._session.execute(statement)
        await self._session.flush()
        return result.scalar_one_or_none() is not None

    async def set_status(
        self,
        group_id: str,
        status: PurchaseStatus,
        completed_at: Optional[datetime] = None,
    ) -> None:
        statement = (
            update(GroupPurchase)
            .where(GroupPurchase.id == group_id)
            .values(status=status, completed_at=completed_at)
        )
        await self._session.execute(statement)
        await self._session.flush()

    async def list_by_user(self, user_id: str) -> List[UserGroupPurchaseDTO]:
        """Все закупки пользователя (как организатор или участник)."""
        statement = (
            select(GroupPurchase)
            .join(GroupParticipant, GroupParticipant.group_id == GroupPurchase.id)
            .where(GroupParticipant.user_id == user_id)
            .order_by(GroupPurchase.created_at.desc())
        )
        result = await self._session.execute(statement)
        groups = result.scalars().all()

        roles_stmt = (
            select(GroupParticipant.group_id, GroupParticipant.role)
            .where(GroupParticipant.user_id == user_id)
        )
        roles_result = await self._session.execute(roles_stmt)
        roles_map = {row.group_id: row.role for row in roles_result}

        product_ids = [g.product_id for g in groups]
        products_stmt = select(Product).where(Product.id.in_(product_ids))
        products_result = await self._session.execute(products_stmt)
        products_map = {p.id: p.name for p in products_result}

        return [
            UserGroupPurchaseDTO(
                id=g.id,
                product_name=products_map.get(g.product_id, "Unknown"),
                status=g.status,
                role=roles_map.get(g.id, "PARTICIPANT"),
                current_joined_count=g.current_joined_count,
                target_size=g.target_size,
                expires_at=g.expires_at,
                invite_code=g.invite_code if g.organizer_id == user_id else None,
            )
            for g in groups
        ]

    async def list_expired(self, now: datetime) -> List[GroupPurchase]:
        """Просроченные активные закупки (для фоновой задачи отмены)."""
        statement = (
            select(GroupPurchase)
            .where(
                GroupPurchase.status == PurchaseStatus.ACTIVE,
                GroupPurchase.expires_at <= now,
            )
            .with_for_update(skip_locked=True)
        )
        result = await self._session.execute(statement)
        return result.scalars().all()