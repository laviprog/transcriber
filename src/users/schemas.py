from pydantic import UUID4

from src.schemas import BaseSchema


class User(BaseSchema):
    id: UUID4
    username: str
    is_active: bool
    role: str


class UserCreate(BaseSchema):
    username: str
    password: str


class UserList(BaseSchema):
    users: list[User]
