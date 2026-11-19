from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.api.router import api_router


app = FastAPI(
    title=settings.app_name,
    description=(
        "Enterprise Multimodal Agentic Intelligence Platform"
    ),
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "architecture": "Modular Enterprise API",
        "documentation": "/docs"
    }


app.include_router(
    api_router,
    prefix=settings.api_prefix
)
