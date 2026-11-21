from ...interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.items import ItemDTO


class GetItemUsecase:

    async def __call__(
        self,

        uow: UnitOfWorkInterface,
        item_id: str,
    ) -> ItemDTO | None:

        item = await uow.items.get_item(item_id)

        return item
