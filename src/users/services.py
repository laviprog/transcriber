from advanced_alchemy.extensions.fastapi import service

from src.auth.security.passwords import hash_password
from src.users.models import UserModel
from src.users.repositories import UserRepository


class UserService(
    service.SQLAlchemyAsyncRepositoryService[UserModel, UserRepository]
):
    """User Service"""

    repository_type = UserRepository

    async def create_user(self, user_obj: UserModel) -> UserModel:
        user_obj.password = hash_password(user_obj.password)
        return await self.create(user_obj, auto_commit=True)
