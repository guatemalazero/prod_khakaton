from typing import List

from fastapi import APIRouter

from ...deps import (
    uow,
    get_products_list as get_products_list_uc,
    get_product_detail as get_product_detail_uc,
)
from ..schemas import ProductResponse, ProductDetailResponse

router = APIRouter(prefix='/products', tags=['Products'])


@router.get('/', response_model=List[ProductResponse])
async def list_products(
    uow: uow,
    get_products_list: get_products_list_uc,
) -> List[ProductResponse]:
    products = await get_products_list(uow)
    return [ProductResponse.model_validate(p) for p in products]


@router.get('/{product_id}', response_model=ProductDetailResponse)
async def get_product(
    product_id: str,
    uow: uow,
    get_product_detail: get_product_detail_uc,
) -> ProductDetailResponse:
    product = await get_product_detail(uow, product_id)
    return ProductDetailResponse.model_validate(product)
