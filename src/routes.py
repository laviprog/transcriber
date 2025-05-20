from datetime import datetime

from fastapi import APIRouter
from scalar_fastapi import get_scalar_api_reference

from src.schemas import HealthCheck

router = APIRouter(tags=["Monitoring"])


@router.get(
    "/healthcheck",
    summary="Health Check",
    description="""
        Checks whether the API service is operational and responding
    """,
    responses={
        200: {
            "description": "Service is running",
        },
    },
)
async def healthcheck() -> HealthCheck:
    return HealthCheck(timestamp=datetime.utcnow().isoformat())


@router.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="Speech Transcription API",
    )
