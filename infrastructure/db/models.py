import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ._service.base import Base
from ...domain.enums import GroupBuyStatus, UserRole

pk = Annotated[str, mapped_column(primary_key=True, default=lambda: str(secrets.token_urlsafe(5)))]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[pk]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    role: Mapped[str] = mapped_column(default=UserRole.USER)

    # Список групповых закупок, в которых участвует пользователь
    group_buys: Mapped[list["GroupBuy"]] = relationship(
        secondary="user_buys",
        back_populates="users",
    )


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[pk]
    name: Mapped[str]
    price: Mapped[int]
    group_price: Mapped[int]


class GroupBuyTerms(Base):
    __tablename__ = 'group_buys_terms'

    id: Mapped[pk]
    item_id: Mapped[str] = mapped_column(ForeignKey('items.id'))
    people_count: Mapped[int]


class GroupBuy(Base):
    __tablename__ = 'group_buys'

    id: Mapped[pk]
    status: Mapped[str] = mapped_column(default=GroupBuyStatus.PENDING)
    current_people_count: Mapped[int] = mapped_column(default=1)
    current_money_count: Mapped[int] = mapped_column(default=0)

    item_id: Mapped[str] = mapped_column(ForeignKey('items.id'))
    url: Mapped[str]
    expire: Mapped[int] = mapped_column(
        default=lambda: int(datetime.now(timezone.utc).timestamp() + timedelta(hours=10).total_seconds())
    )

    users: Mapped[list["User"]] = relationship(
        secondary="user_buys",
        back_populates="group_buys",
    )


class UserBuy(Base):
    __tablename__ = 'user_buys'

    id: Mapped[pk]
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    group_buy_id: Mapped[str] = mapped_column(ForeignKey('group_buys.id'))
