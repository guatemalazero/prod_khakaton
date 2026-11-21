from typing import Optional

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.products import ProductDetailDTO


class GetProductDetailUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        product_id: str,
    ) -> Optional[ProductDetailDTO]:
        return await uow.products.get_by_id(product_id)
