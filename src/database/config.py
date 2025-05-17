from advanced_alchemy.extensions.fastapi import (
    AdvancedAlchemy,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)
from fastapi import FastAPI

from src.config import settings

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.DB_URL,
    session_config=session_config,
)
alchemy = AdvancedAlchemy(config=sqlalchemy_config)


def init_alchemy(app: FastAPI) -> None:
    alchemy.init_app(app)
