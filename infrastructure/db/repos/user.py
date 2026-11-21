from typing import Any

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ....domain.dtos.user import UserDTO, UpdateUserDTO
from ....domain.dtos.group_buy import GroupBuyDTO


class UsersRepo:
    def __init__(self, async_session: AsyncSession):
        self._session = async_session

    async def create_user(self, data: dict[str, Any]) -> str:
        instance = User(**data)
        self._session.add(instance)
        await self._session.flush()
        return instance.id

    async def get_user(self, login: str) -> UserDTO | None:
        statement = (
            select(User)
            .options(selectinload(User.group_buys))
            .where(User.login == login)
        )
        result = await self._session.execute(statement)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return UserDTO(
            id=user.id,
            login=user.login,
            password=user.password,
            role=user.role,
            group_buys=[
                GroupBuyDTO(
                    id=group_buy.id,
                    status=group_buy.status,
                    current_people_count=group_buy.current_people_count,
                    current_money_count=group_buy.current_money_count,
                    item_id=group_buy.item_id,
                    url=group_buy.url,
                    expire=group_buy.expire,
                )
                for group_buy in user.group_buys
            ],
        )

    async def update_user(self, login: str, patches: UpdateUserDTO) -> None:
        statement = (
            update(User)
            .where(User.login == login)
            .values(**patches.to_dict())
        )
        
        await self._session.execute(statement)
        await self._session.flush()