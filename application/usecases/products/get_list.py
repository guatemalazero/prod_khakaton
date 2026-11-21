from typing import List

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.products import ProductDTO


class GetProductsListUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ProductDTO]:
        return await uow.products.list_all(limit=limit, offset=offset)
