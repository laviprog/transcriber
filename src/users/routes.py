from uuid import UUID

from fastapi import APIRouter

from src.auth.security.dependencies import CurrentAdminDep
from src.auth.security.passwords import hash_password
from src.users.dependencies import UserServiceDep
from src.users.models import UserModel
from src.users.schemas import User, UserCreate, UserList

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str, service: UserServiceDep, admin: CurrentAdminDep
) -> User | None:
    user = await service.get(UUID(user_id))
    if not user:
        return None
    return user


@router.get("", response_model=UserList)
async def get_all_users(
    service: UserServiceDep, admin: CurrentAdminDep
) -> UserList:
    users = await service.list()
    return UserList(users=users)


@router.post("", response_model=User)
async def create_user(user: UserCreate, service: UserServiceDep) -> User:
    user_data = user.model_dump(exclude_unset=True, exclude_none=True)
    user_data["password"] = hash_password(user.password)

    created_user = await service.create(
        UserModel(**user_data), auto_commit=True
    )
    return created_user
