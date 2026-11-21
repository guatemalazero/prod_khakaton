from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import GroupBuy, UserBuy, Item, User
from ....domain.dtos.group_buy import GroupBuyDTO


class GroupBuyRepo:
    def __init__(self, async_session: AsyncSession):
        self._session = async_session

    async def create_group_buy(self, item_id: str) -> str:
        # url не передаётся эндпоинтом, поэтому собираем его из id уже
        # после первого flush (id генерируется сервером по умолчанию)
        instance = GroupBuy(item_id=item_id, url='')
        self._session.add(instance)
        await self._session.flush()

        instance.url = f'/group_buy/{instance.id}'
        await self._session.flush()

        return instance.id

    async def get_group_buy(self, group_buy_id: str) -> Optional[GroupBuyDTO]:
        statement = select(GroupBuy).where(GroupBuy.id == group_buy_id)
        result = await self._session.execute(statement)
        group_buy = result.scalar_one_or_none()

        if group_buy is None:
            return None

        return GroupBuyDTO(
            id=group_buy.id,
            status=group_buy.status,
            current_people_count=group_buy.current_people_count,
            current_money_count=group_buy.current_money_count,
            item_id=group_buy.item_id,
            url=group_buy.url,
            expire=group_buy.expire,
        )

    async def add_user(self, group_buy_id: str, user_login: str) -> None:
        statement = select(User.id).where(User.login == user_login)
        result = await self._session.execute(statement)
        user_id = result.scalar_one_or_none()

        if user_id is None:
            return None

        instance = UserBuy(user_id=user_id, group_buy_id=group_buy_id)
        self._session.add(instance)

        statement = (
            update(GroupBuy)
            .where(GroupBuy.id == group_buy_id)
            .values(current_people_count=GroupBuy.current_people_count + 1)
        )
        await self._session.execute(statement)
        await self._session.flush()

    async def test_payment(self, group_buy_id: str) -> None:
        statement = (
            select(Item.group_price)
            .join(GroupBuy, GroupBuy.item_id == Item.id)
            .where(GroupBuy.id == group_buy_id)
        )
        result = await self._session.execute(statement)
        group_price = result.scalar_one_or_none()

        if group_price is None:
            return None

        statement = (
            update(GroupBuy)
            .where(GroupBuy.id == group_buy_id)
            .values(current_money_count=GroupBuy.current_money_count + group_price)
        )
        await self._session.execute(statement)
        await self._session.flush()