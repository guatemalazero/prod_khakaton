from fastapi import FastAPI
from contextlib import asynccontextmanager

from .api.endpoints.group_purchases import router as group_purchases_router
from .api.endpoints.orders import router as orders_router
from .api.endpoints.products import router as products_router
from .api.endpoints.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.include_router(group_purchases_router)
    app.include_router(products_router)
    app.include_router(orders_router)
    app.include_router(users_router)
    yield


app = FastAPI(
    title="API групповых закупок",
    description=(
        "API для совместных (групповых) покупок: создание закупок, вступление по invite-коду, "
        "создание и оплата заказов, просмотр кошелька, транзакций и личного кабинета.\n\n"
        "Авторизация для хакатона: передавайте заголовок `X-User-Name` с именем пользователя. "
        "Если пользователь не существует — он создаётся автоматически вместе с кошельком."
    ),
    version="1.0.0",
    lifespan=lifespan,
    contact={"name": "Команда хакатона"},
    openapi_tags=[
        {"name": "Products", "description": "Каталог товаров"},
        {"name": "Group Purchases", "description": "Создание, вступление и просмотр групповых закупок"},
        {"name": "Orders", "description": "Создание и оплата заказов"},
        {"name": "User Cabinet", "description": "Личный кошелёк, транзакции, заказы и закупки"},
    ],
)