from fastapi import FastAPI
from contextlib import asynccontextmanager

from .api.endpoints.group_buy import router as gb_router
from .api.endpoints.items import router as items_router
from .api.endpoints.user import router as user_router

async def fastapi_bootstrap(app: FastAPI):
    app.include_router(gb_router)
    app.include_router(items_router)
    app.include_router(user_router)

    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    await fastapi_bootstrap(app)

    yield

app = FastAPI(lifespan=lifespan)