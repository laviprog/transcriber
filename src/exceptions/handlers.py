from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src import log


def setup_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        log.error(
            f"HTTPException [{request.method} {request.url}]: {exc.detail}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            headers=exc.headers or {},
            content={
                "detail": exc.detail,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        log.error(
            f"RequestValidationError [{request.method} {request.url}]: {exc.errors()}",
        )

        return JSONResponse(
            status_code=422,
            content={
                "detail": exc.errors(),
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        log.error(
            f"Unhandled Exception [{request.method} {request.url}]: {str(exc)}",
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "An unexpected error occurred",
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
