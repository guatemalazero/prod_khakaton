from typing import Protocol

from ......domain.enums import ParticipantRole


class GroupParticipantRepositoryInterface(Protocol):
    async def add(self, group_id: str, user_id: str, role: ParticipantRole) -> str: ...
    async def exists(self, group_id: str, user_id: str) -> bool: ...