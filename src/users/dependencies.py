from typing import Annotated, AsyncGenerator

from fastapi import Depends

from src.database.config import sqlalchemy_config
from src.users.services import UserService


async def provide_user_service() -> AsyncGenerator[UserService, None]:
    async with UserService.new(config=sqlalchemy_config) as service:
        yield service


UserServiceDep = Annotated[UserService, Depends(provide_user_service)]
