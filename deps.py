from fastapi import Depends
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

from .infrastructure.db.uow import UnitOfWork
from .infrastructure.redis_client import RedisClient
from .services.func import Func

# Singletones

redis = Redis()

# DB Dependencies

engine = create_async_engine('postgresql+asyncpg://postgres:Gareefac123@localhost:5432/dsfJfsfasd')
session_factory = async_sessionmaker(engine)

# Clients

redis_client = RedisClient(engine=redis)

# Services

func_service = Func()

# Usecases

register_usecase = RegisterUserUsecase(redis_client=redis_client, func_service=func_service)
login_usecase = LoginUserUsecase(redis_client=redis_client, func_service=func_service)
get_user_usecase = GetUserUsecase()

get_item_usecase = GetItemUsecase()
get_items_usecase = GetItemsUsecase()

create_group_buy_usecase = CreateGroupBuyUsecase()
get_group_buy_usecase = GetGroupBuyUsecase()
add_user_usecase = AddUserUsecase()
test_payment_usecase = TestPaymentUsecase()

# get Функции
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

# Annotated
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