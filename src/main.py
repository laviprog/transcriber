from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database.config import init_alchemy
from src.routes import router
from src.users.routes import router as user_router
from src.auth.routes import router as auth_router

app = FastAPI(
    title="Voice Recognition API",
    version="0.0.1",
    docs_url="/docs/swagger",
    redoc_url="/docs/redoc",
    openapi_url="/openapi.json",
    root_path="/api/v1",
)

init_alchemy(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router)
app.include_router(router=user_router)
app.include_router(router=auth_router)
