from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(
    prefix="/health",
    tags=["System Health"]
)

@router.get("/")
async def health():

    return {
        "status": "healthy",
        "application": "NEXUS AI",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/details")
async def health_details():

    return {
        "backend": "Online",
        "api": "Operational",
        "ai_engine": "Not Connected",
        "database": "Not Connected",
        "vector_store": "Not Connected"
    }
