from src.schemas import BaseSchema


class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class Refresh(BaseSchema):
    refresh_token: str


class Login(BaseSchema):
    username: str
    password: str
