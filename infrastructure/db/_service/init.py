from .base import Base
import asyncio
from ..models import *
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_async_engine('postgresql+asyncpg://postgres:Gareefac123@localhost:5432/dsfJfsfasd', echo=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(create_tables())