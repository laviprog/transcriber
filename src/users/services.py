from advanced_alchemy.extensions.fastapi import service

from src.users.models import UserModel
from src.users.repositories import UserRepository


class UserService(
    service.SQLAlchemyAsyncRepositoryService[UserModel, UserRepository]
):
    """User Service"""

    repository_type = UserRepository
