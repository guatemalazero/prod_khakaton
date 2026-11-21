from ...interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.items import ItemDTO


class GetItemsUsecase:

    async def __call__(
        self,

        uow: UnitOfWorkInterface,
    ) -> list[ItemDTO]:

        items = await uow.items.get_items()

        return items
