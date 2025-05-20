from advanced_alchemy.extensions.fastapi import repository

from src.users.models import UserModel


class UserRepository(repository.SQLAlchemyAsyncRepository[UserModel]):
    """User repository"""

    model_type = UserModel
