from fastapi import Depends, Header
from redis import Redis
from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from .application.usecases.user.register import RegisterUserUsecase
from .application.usecases.user.login import LoginUserUsecase
from .application.usecases.user.get import GetUserUsecase
from .application.usecases.item.get_item import GetItemUsecase
from .application.usecases.item.get_items import GetItemsUsecase
from .application.usecases.group_buy.create import CreateGroupBuyUsecase
from .application.usecases.group_buy.get import GetGroupBuyUsecase
from .application.usecases.group_buy.add_user import AddUserUsecase
from .application.usecases.group_buy.test_payment import TestPaymentUsecase
from .application.usecases.group_purchase.create import CreateGroupPurchaseUsecase
from .application.usecases.group_purchase.get import GetGroupPurchaseUsecase
from .application.usecases.group_purchase.join import JoinGroupPurchaseUsecase
from .application.usecases.order.create import CreateOrderUsecase
from .application.usecases.order.pay import PayOrderUsecase
from .application.usecases.user.get_wallet import GetUserWalletUsecase
from .application.usecases.user.get_transactions import GetUserTransactionsUsecase
from .application.usecases.user.get_orders import GetUserOrdersUsecase
from .application.usecases.user.get_group_purchases import GetUserGroupPurchasesUsecase
from .application.usecases.product.get_list import GetProductsListUsecase
from .application.usecases.product.get_detail import GetProductDetailUsecase

from .infrastructure.db.uow import UnitOfWork
from .infrastructure.db.models import User
from .infrastructure.redis_client import RedisClient
from .services.func import Func

# =====================================================================
# Singletons
# =====================================================================
redis = Redis()

# =====================================================================
# DB Dependencies
# =====================================================================
engine = create_async_engine('postgresql+asyncpg://postgres:Gareefac123@localhost:5432/dsfJfsfasd')
session_factory = async_sessionmaker(engine)

# =====================================================================
# Clients
# =====================================================================
redis_client = RedisClient(engine=redis)

# =====================================================================
# Services
# =====================================================================
func_service = Func()

# =====================================================================
# Usecases (старые)
# =====================================================================
register_usecase = RegisterUserUsecase(redis_client=redis_client, func_service=func_service)
login_usecase = LoginUserUsecase(redis_client=redis_client, func_service=func_service)
get_user_usecase = GetUserUsecase()
get_item_usecase = GetItemUsecase()
get_items_usecase = GetItemsUsecase()
create_group_buy_usecase = CreateGroupBuyUsecase()
get_group_buy_usecase = GetGroupBuyUsecase()
add_user_usecase = AddUserUsecase()
test_payment_usecase = TestPaymentUsecase()

# =====================================================================
# Usecases (новые под SQL-схему)
# =====================================================================
create_group_purchase_usecase = CreateGroupPurchaseUsecase()
get_group_purchase_usecase = GetGroupPurchaseUsecase()
join_group_purchase_usecase = JoinGroupPurchaseUsecase()
create_order_usecase = CreateOrderUsecase()
pay_order_usecase = PayOrderUsecase()
get_user_wallet_usecase = GetUserWalletUsecase()
get_user_transactions_usecase = GetUserTransactionsUsecase()
get_user_orders_usecase = GetUserOrdersUsecase()
get_user_group_purchases_usecase = GetUserGroupPurchasesUsecase()
get_products_list_usecase = GetProductsListUsecase()
get_product_detail_usecase = GetProductDetailUsecase()

# =====================================================================
# Зависимости (Depends функции)
# =====================================================================
async def get_uow():
    async with UnitOfWork(session_factory=session_factory) as uow:
        yield uow

async def get_register_usecase():
    yield register_usecase

async def get_login_usecase():
    yield login_usecase

async def get_user_usecase_dep():
    yield get_user_usecase

async def get_item_usecase_dep():
    yield get_item_usecase

async def get_items_usecase_dep():
    yield get_items_usecase

async def get_create_group_buy_usecase_dep():
    yield create_group_buy_usecase

async def get_get_group_buy_usecase_dep():
    yield get_group_buy_usecase

async def get_add_user_usecase():
    yield add_user_usecase

async def get_test_payment_usecase():
    yield test_payment_usecase

# Новые зависимости
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

# =====================================================================
# Зависимость для получения user_id из заголовка (для хакатона)
# =====================================================================
async def get_current_user_id(
    x_user_name: str = Header(..., alias="X-User-Name", description="Имя пользователя (для хакатона)"),
    uow: UnitOfWorkInterface = Depends(get_uow),
) -> int:
    """
    Для хакатона без авторизации: извлекает user_id из заголовка X-User-Name.
    Если пользователь не найден — создаёт его.
    """
    user = await uow.users.get_by_name(x_user_name)
    
    if not user:
        user = User(name=x_user_name)
        user = await uow.users.add(user)
        await uow.commit()
    
    return user.id

# =====================================================================
# Annotated типы для использования в эндпоинтах
# =====================================================================
uow = Annotated[UnitOfWorkInterface, Depends(get_uow)]
register = Annotated[RegisterUserUsecase, Depends(get_register_usecase)]
login = Annotated[LoginUserUsecase, Depends(get_login_usecase)]
get_user = Annotated[GetUserUsecase, Depends(get_user_usecase_dep)]
get_item = Annotated[GetItemUsecase, Depends(get_item_usecase_dep)]
get_items = Annotated[GetItemsUsecase, Depends(get_items_usecase_dep)]
create_group_buy = Annotated[CreateGroupBuyUsecase, Depends(get_create_group_buy_usecase_dep)]
get_group_buy = Annotated[GetGroupBuyUsecase, Depends(get_get_group_buy_usecase_dep)]
add_user = Annotated[AddUserUsecase, Depends(get_add_user_usecase)]
test_payment = Annotated[TestPaymentUsecase, Depends(get_test_payment_usecase)]

# Новые Annotated типы
create_group_purchase = Annotated[CreateGroupPurchaseUsecase, Depends(get_create_group_purchase_usecase_dep)]
get_group_purchase = Annotated[GetGroupPurchaseUsecase, Depends(get_get_group_purchase_usecase_dep)]
join_group_purchase = Annotated[JoinGroupPurchaseUsecase, Depends(get_join_group_purchase_usecase_dep)]
create_order = Annotated[CreateOrderUsecase, Depends(get_create_order_usecase_dep)]
pay_order = Annotated[PayOrderUsecase, Depends(get_pay_order_usecase_dep)]
get_user_wallet = Annotated[GetUserWalletUsecase, Depends(get_user_wallet_usecase_dep)]
get_user_transactions = Annotated[GetUserTransactionsUsecase, Depends(get_user_transactions_usecase_dep)]
get_user_orders = Annotated[GetUserOrdersUsecase, Depends(get_user_orders_usecase_dep)]
get_user_group_purchases = Annotated[GetUserGroupPurchasesUsecase, Depends(get_user_group_purchases_usecase_dep)]
get_products_list = Annotated[GetProductsListUsecase, Depends(get_products_list_usecase_dep)]
get_product_detail = Annotated[GetProductDetailUsecase, Depends(get_product_detail_usecase_dep)]

# Зависимость для user_id
current_user_id = Annotated[int, Depends(get_current_user_id)]