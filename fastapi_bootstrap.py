from fastapi import FastAPI
from contextlib import asynccontextmanager

async def fastapi_bootstrap(app: FastAPI):
    # Тут boostrap

    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    await fastapi_bootstrap(app)

    yield

app = FastAPI(lifespan=lifespan)