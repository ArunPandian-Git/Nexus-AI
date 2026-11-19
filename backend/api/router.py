from fastapi import APIRouter

from backend.api.routes import (
    health,
    chat,
    documents,
    agents,
    analytics
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(documents.router)
api_router.include_router(agents.router)
api_router.include_router(analytics.router)
