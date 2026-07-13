import secrets
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column
from ._service.base import Base

pk = Annotated[str, mapped_column(primary_key=True, default=lambda: str(secrets.token_urlsafe(5)))]

class BaseTable(Base):
    pass