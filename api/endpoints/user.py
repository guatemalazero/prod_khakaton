from fastapi import APIRouter
from ...deps import (
    uow
)

from ..schemas.user import AuthModel
from ...domain.dtos.user import UserDTO

router = APIRouter(prefix='/user')

@router.post('/register')
async def _(
    payload: AuthModel,

    uow: uow,
    # register_user: ...
) -> UserDTO:
    pass

@router.post('/login')
async def _(
    payload: AuthModel,

    uow: uow,
    # login_user: ...
) -> UserDTO:
    pass

@router.get('/get/{user_login}')
async def _(
    login: str,

    uow: uow,
    # get_user: ... 
) -> UserDTO:
    pass