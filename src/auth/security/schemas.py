from uuid import UUID

from pydantic import BaseModel

from src.users.models import Role


class TokenPayload(BaseModel):
    id: UUID
    role: Role
