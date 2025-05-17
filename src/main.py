from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.lifecycle import lifespan
from src.routes import router

app = FastAPI(
    title="Voice Recognition API",
    version="0.0.1",
    docs_url="/docs/swagger",
    redoc_url="/docs/redoc",
    openapi_url="/openapi.json",
    root_path="/api/v1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router)
