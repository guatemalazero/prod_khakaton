from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .application.interfaces.infrastructure.db.uow import UnitOfWorkInterface

from .infrastructure.db.uow import UnitOfWork

# DB Dependencies

engine = create_async_engine('postgresql+asyncpg://postgres:Gareefac123@localhost:5432/dsfJfsfasd')
session_factory = async_sessionmaker(engine)

# get Функции
async def get_uow():
    async with UnitOfWork(session_factory=session_factory) as uow:
        yield uow

# Annotated
uow = Annotated[UnitOfWorkInterface, Depends(get_uow)]