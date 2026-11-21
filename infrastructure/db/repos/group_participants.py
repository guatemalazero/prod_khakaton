from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import GroupParticipant
from ....domain.enums import ParticipantRole


class GroupParticipantRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, group_id: int, user_id: str, role: ParticipantRole) -> str:
        participant = GroupParticipant(
            group_id=group_id,
            user_id=user_id,
            role=role,
        )
        self._session.add(participant)
        await self._session.flush()
        return participant.id

    async def exists(self, group_id: int, user_id: str) -> bool:
        statement = select(GroupParticipant).where(
            GroupParticipant.group_id == group_id,
            GroupParticipant.user_id == user_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none() is not None