from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Product
from ....domain.dtos.products import ProductDetailDTO, ProductDTO


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, product_id: str) -> Optional[ProductDetailDTO]:
        statement = select(Product).where(Product.id == product_id)
        result = await self._session.execute(statement)
        product = result.scalar_one_or_none()

        if product is None:
            return None

        return ProductDetailDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            regular_price=product.regular_price,
            base_group_price=product.base_group_price,
            pricing_rules=product.pricing_rules or [],
            min_participants=product.min_participants,
            max_participants=product.max_participants,
            time_limit_minutes=product.time_limit_minutes,
            organizer_reward_percent=product.organizer_reward_percent,
        )

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[ProductDTO]:
        statement = (
            select(Product)
            .order_by(Product.id)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(statement)
        products = result.scalars().all()

        return [
            ProductDTO(
                id=p.id,
                name=p.name,
                regular_price=p.regular_price,
                base_group_price=p.base_group_price,
                min_participants=p.min_participants,
                max_participants=p.max_participants,
            )
            for p in products
        ]