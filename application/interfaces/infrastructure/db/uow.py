from typing import Protocol

class UnitOfWorkInterface(Protocol):
    

    async def commit(self) -> None: ...