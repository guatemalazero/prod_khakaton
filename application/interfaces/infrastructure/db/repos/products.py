from typing import Protocol, Optional, List

from ......domain.dtos.products import ProductDTO, ProductDetailDTO


class ProductRepositoryInterface(Protocol):
    async def get_by_id(self, product_id: str) -> Optional[ProductDetailDTO]: ...
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[ProductDTO]: ...