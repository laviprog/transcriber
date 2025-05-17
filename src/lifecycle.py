from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import init_alchemy


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_alchemy(app)
    yield
