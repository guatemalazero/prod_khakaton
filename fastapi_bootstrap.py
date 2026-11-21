from fastapi import FastAPI
from contextlib import asynccontextmanager

from .api.endpoints.group_purchases import router as group_purchases_router
from .api.endpoints.orders import router as orders_router
from .api.endpoints.products import router as products_router
from .api.endpoints.users import router as users_router

async def fastapi_bootstrap(app: FastAPI):
    app.include_router(group_purchases_router)
    app.include_router(products_router)
    app.include_router(orders_router)
    app.include_router(users_router)

    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    await fastapi_bootstrap(app)

    yield

app = FastAPI(lifespan=lifespan)