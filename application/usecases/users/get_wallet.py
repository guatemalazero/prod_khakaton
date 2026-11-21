from typing import Optional

from ....application.interfaces.infrastructure.db.uow import UnitOfWorkInterface
from ....domain.dtos.user import WalletDTO


class GetUserWalletUsecase:
    async def __call__(
        self,
        uow: UnitOfWorkInterface,
        user_id: str,
    ) -> Optional[WalletDTO]:
        return await uow.wallets.get_by_user_id(user_id)
