from fastapi import APIRouter
from scalar_fastapi import get_scalar_api_reference

router = APIRouter()


@router.get("/healthcheck", summary="Health Check", tags=["Monitoring"])
async def healthcheck():
    return {"status": "ok"}


@router.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="Voice Recognition API",
    )
