from typing import Optional

from fastapi import APIRouter, HTTPException
from ...deps import (
    uow,
    register as register_uc,
    login as login_uc,
    get_user as get_user_uc,
)

from ..schemas.user import AuthModel
from ...domain.dtos.user import (
    UserDTO,
    AuthUserDTO
)

router = APIRouter(prefix='/user')

@router.post('/register')
async def _(
    payload: AuthModel,

    uow: uow,
    register_user: register_uc,
    get_user: get_user_uc,
) -> UserDTO:
    dto = AuthUserDTO(**payload.model_dump())

    await register_user(dto, uow)

    user = await get_user(uow, dto.login)

    return user

@router.post('/login')
async def _(
    payload: AuthModel,

    uow: uow,
    login_user: login_uc,
    get_user: get_user_uc,
) -> UserDTO:
    dto = AuthUserDTO(**payload.model_dump())

    session_string = await login_user(dto, uow)

    if session_string is None:
        raise HTTPException(status_code=401, detail='Invalid login or password')

    user = await get_user(uow, dto.login)

    return user

@router.get('/get/{user_login}')
async def _(
    user_login: str,

    uow: uow,
    get_user: get_user_uc,
) -> Optional[UserDTO]:
    user = await get_user(uow, user_login)

    return user
