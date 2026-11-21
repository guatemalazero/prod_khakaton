import secrets
from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated, Optional, List

from sqlalchemy import ForeignKey, String, Numeric, Text, JSON, DateTime, UniqueConstraint, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._service.base import Base
from ...domain.enums import (
    PurchaseStatus,
    ParticipantRole,
    OrderStatus,
    TransactionType,
)

pk = Annotated[str, mapped_column(primary_key=True, default=lambda: secrets.token_urlsafe(5))]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    wallet: Mapped[Optional["Wallet"]] = relationship(back_populates="user", uselist=False)
    group_participants: Mapped[List["GroupParticipant"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")
    organized_purchases: Mapped[List["GroupPurchase"]] = relationship(
        foreign_keys="[GroupPurchase.organizer_id]", back_populates="organizer"
    )


class Wallet(Base):
    __tablename__ = 'wallets'

    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), primary_key=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))

    user: Mapped["User"] = relationship(back_populates="wallet")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    regular_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    base_group_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    pricing_rules: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    min_participants: Mapped[int]
    max_participants: Mapped[int]
    time_limit_minutes: Mapped[int]
    organizer_reward_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"))

    group_purchases: Mapped[List["GroupPurchase"]] = relationship(back_populates="product")


class GroupPurchase(Base):
    __tablename__ = 'group_purchases'

    id: Mapped[pk]
    product_id: Mapped[str] = mapped_column(ForeignKey('products.id'))
    organizer_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    status: Mapped[str] = mapped_column(default=PurchaseStatus.ACTIVE.value)
    target_size: Mapped[int]
    current_joined_count: Mapped[int] = mapped_column(default=1)
    current_paid_count: Mapped[int] = mapped_column(default=0)
    invite_code: Mapped[str] = mapped_column(String(32), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    product: Mapped["Product"] = relationship(back_populates="group_purchases")
    organizer: Mapped["User"] = relationship(foreign_keys=[organizer_id], back_populates="organized_purchases")
    participants: Mapped[List["GroupParticipant"]] = relationship(back_populates="group_purchase")
    orders: Mapped[List["Order"]] = relationship(back_populates="group_purchase")


class GroupParticipant(Base):
    __tablename__ = 'group_participants'
    __table_args__ = (
        UniqueConstraint('group_id', 'user_id', name='uq_group_participant'),
    )

    id: Mapped[pk]
    group_id: Mapped[str] = mapped_column(ForeignKey('group_purchases.id'))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    role: Mapped[str] = mapped_column(default=ParticipantRole.PARTICIPANT.value)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    group_purchase: Mapped["GroupPurchase"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship(back_populates="group_participants")


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        UniqueConstraint('group_id', 'user_id', name='uq_order_group_user'),
    )

    id: Mapped[pk]
    group_id: Mapped[str] = mapped_column(ForeignKey('group_purchases.id'))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[str] = mapped_column(ForeignKey('products.id'))
    fixed_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(default=OrderStatus.PENDING.value)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(64), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    group_purchase: Mapped["GroupPurchase"] = relationship(back_populates="orders")
    user: Mapped["User"] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship()
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="order")


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[pk]
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    order_id: Mapped[Optional[str]] = mapped_column(ForeignKey('orders.id'), nullable=True)
    type: Mapped[str] = mapped_column(default=TransactionType.PAYMENT.value)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship(back_populates="transactions")
    order: Mapped["Order"] = relationship(back_populates="transactions")
