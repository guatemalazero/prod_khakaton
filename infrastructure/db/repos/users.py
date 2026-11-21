from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User, Wallet
from ....domain.dtos.user import UserDTO


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, name: str) -> str:
        user = User(name=name)
        self._session.add(user)
        await self._session.flush()

        wallet = Wallet(user_id=user.id, balance=0)
        self._session.add(wallet)
        await self._session.flush()

        return user.id

    async def get_by_id(self, user_id: str) -> Optional[UserDTO]:
        statement = select(User).where(User.id == user_id)
        result = await self._session.execute(statement)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return UserDTO(
            id=user.id,
            name=user.name,
            created_at=user.created_at,
        )

    async def get_by_name(self, name: str) -> Optional[UserDTO]:
        statement = select(User).where(User.name == name)
        result = await self._session.execute(statement)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return UserDTO(
            id=user.id,
            name=user.name,
            created_at=user.created_at,
        )
