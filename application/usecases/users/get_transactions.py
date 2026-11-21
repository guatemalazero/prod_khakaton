from typing import List

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.user import TransactionDTO


class GetUserTransactionUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        user_id: str,
    ) -> List[TransactionDTO]:
        return await uow.transactions.list_by_user(user_id)
