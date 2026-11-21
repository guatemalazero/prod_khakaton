from fastapi import Depends, Header
from redis import Redis
from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from .application.usecases.group_purchases.create import CreateGroupPurchaseUsecase
from .application.usecases.group_purchases.get import GetGroupPurchaseUsecase
from .application.usecases.group_purchases.join import JoinGroupPurchaseUsecase
from .application.usecases.orders.create import CreateOrderUsecase
from .application.usecases.orders.pay import PayOrderUsecase
from .application.usecases.users.get_wallet import GetUserWalletUsecase
from .application.usecases.users.get_transactions import GetUserTransactionUsecase
from .application.usecases.users.get_orders import GetUserOrdersUsecase
from .application.usecases.users.get_group_purchases import GetUserGroupPurchaseUsecase
from .application.usecases.products.get_list import GetProductsListUsecase
from .application.usecases.products.get_detail import GetProductDetailUsecase
from .infrastructure.db.uow import UnitOfWork
from .infrastructure.db.models import User
from .infrastructure.redis_client import RedisClient
from .services.func import Func

redis = Redis()
engine = create_async_engine('postgresql+asyncpg://postgres:Gareefac123@localhost:5432/dsfJfsfasd')
session_factory = async_sessionmaker(engine)
redis_client = RedisClient(engine=redis)
func_service = Func()

create_group_purchase_usecase = CreateGroupPurchaseUsecase()
get_group_purchase_usecase = GetGroupPurchaseUsecase()
join_group_purchase_usecase = JoinGroupPurchaseUsecase()
create_order_usecase = CreateOrderUsecase()
pay_order_usecase = PayOrderUsecase()
get_user_wallet_usecase = GetUserWalletUsecase()
get_user_transactions_usecase = GetUserTransactionUsecase()
get_user_orders_usecase = GetUserOrdersUsecase()
get_user_group_purchases_usecase = GetUserGroupPurchaseUsecase()
get_products_list_usecase = GetProductsListUsecase()
get_product_detail_usecase = GetProductDetailUsecase()


async def get_uow():
    async with UnitOfWork(session_factory=session_factory) as uow:
        yield uow


async def get_create_group_purchase_usecase_dep():
    yield create_group_purchase_usecase


async def get_get_group_purchase_usecase_dep():
    yield get_group_purchase_usecase


async def get_join_group_purchase_usecase_dep():
    yield join_group_purchase_usecase


async def get_create_order_usecase_dep():
    yield create_order_usecase


async def get_pay_order_usecase_dep():
    yield pay_order_usecase


async def get_user_wallet_usecase_dep():
    yield get_user_wallet_usecase


async def get_user_transactions_usecase_dep():
    yield get_user_transactions_usecase


async def get_user_orders_usecase_dep():
    yield get_user_orders_usecase


async def get_user_group_purchases_usecase_dep():
    yield get_user_group_purchases_usecase


async def get_products_list_usecase_dep():
    yield get_products_list_usecase


async def get_product_detail_usecase_dep():
    yield get_product_detail_usecase


async def get_current_user_id(
    x_user_name: str = Header(..., alias="X-User-Name", description="Имя пользователя (для хакатона)"),
    uow: UnitOfWorkInterface = Depends(get_uow),
) -> str:
    user = await uow.users.get_by_name(x_user_name)
    if not user:
        user_id = await uow.users.create_user(x_user_name)
        await uow.commit()
        return user_id
    return user.id


uow = Annotated[UnitOfWorkInterface, Depends(get_uow)]
create_group_purchase = Annotated[CreateGroupPurchaseUsecase, Depends(get_create_group_purchase_usecase_dep)]
get_group_purchase = Annotated[GetGroupPurchaseUsecase, Depends(get_get_group_purchase_usecase_dep)]
join_group_purchase = Annotated[JoinGroupPurchaseUsecase, Depends(get_join_group_purchase_usecase_dep)]
create_order = Annotated[CreateOrderUsecase, Depends(get_create_order_usecase_dep)]
pay_order = Annotated[PayOrderUsecase, Depends(get_pay_order_usecase_dep)]
get_user_wallet = Annotated[GetUserWalletUsecase, Depends(get_user_wallet_usecase_dep)]
get_user_transactions = Annotated[GetUserTransactionUsecase, Depends(get_user_transactions_usecase_dep)]
get_user_orders = Annotated[GetUserOrdersUsecase, Depends(get_user_orders_usecase_dep)]
get_user_group_purchases = Annotated[GetUserGroupPurchaseUsecase, Depends(get_user_group_purchases_usecase_dep)]
get_products_list = Annotated[GetProductsListUsecase, Depends(get_products_list_usecase_dep)]
get_product_detail = Annotated[GetProductDetailUsecase, Depends(get_product_detail_usecase_dep)]
current_user_id = Annotated[str, Depends(get_current_user_id)]
