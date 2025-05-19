from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.routes import router as auth_router
from src.exceptions.handlers import setup_exception_handlers
from src.exceptions.responses import error_responses
from src.routes import router
from src.users.routes import router as user_router

app = FastAPI(
    title="Voice Recognition API",
    version="0.0.1",
    docs_url="/docs/swagger",
    redoc_url="/docs/redoc",
    openapi_url="/openapi.json",
    root_path="/api/v1",
    responses=error_responses,
)

setup_exception_handlers(app)

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
