%%writefile /content/backend/api/router.py

from fastapi import APIRouter

from backend.api.routes.health import router as health_router
from backend.api.routes.chat import router as chat_router
from backend.api.routes.documents import router as documents_router
from backend.api.routes.agents import router as agents_router
from backend.api.routes.analytics import router as analytics_router
from backend.api.routes.users import router as users_router
from backend.api.routes.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(chat_router)
api_router.include_router(documents_router)
api_router.include_router(agents_router)
api_router.include_router(analytics_router)
api_router.include_router(users_router)
api_router.include_router(auth_router)
