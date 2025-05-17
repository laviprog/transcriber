from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import alchemy
from src.users.services import UserService

SessionDep = Annotated[AsyncSession, Depends(alchemy.provide_session())]


async def provide_user_service(
    session: SessionDep,
) -> AsyncGenerator[UserService, None]:
    async with UserService.new(session=session) as service:
        yield service


UserServiceDep = Annotated[UserService, Depends(provide_user_service)]
