"""
NEXUS AI
Enterprise Multimodal Agentic Intelligence Platform

Backend API — Phase 3
"""

from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# --------------------------------------------------
# APPLICATION CONFIGURATION
# --------------------------------------------------

APP_NAME = "NEXUS AI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "Enterprise Multimodal Agentic Intelligence Platform"
)


# --------------------------------------------------
# FASTAPI INITIALIZATION
# --------------------------------------------------

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# RESPONSE MODELS
# --------------------------------------------------

class HealthResponse(BaseModel):
    application: str
    version: str
    status: str
    timestamp: str


class SystemStatusResponse(BaseModel):
    application: str
    backend: str
    ai_engine: str
    vector_database: str
    relational_database: str


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
async def root():

    return {
        "message": "Welcome to NEXUS AI Backend",
        "application": APP_NAME,
        "version": APP_VERSION,
        "documentation": "/docs",
        "health": "/health",
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"]
)
async def health_check():

    return HealthResponse(
        application=APP_NAME,
        version=APP_VERSION,
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# --------------------------------------------------
# SYSTEM STATUS
# --------------------------------------------------

@app.get(
    "/api/v1/status",
    response_model=SystemStatusResponse,
    tags=["System"]
)
async def system_status():

    return SystemStatusResponse(
        application=APP_NAME,
        backend="Online",
        ai_engine="Not Connected",
        vector_database="Not Connected",
        relational_database="Not Connected",
    )


# --------------------------------------------------
# APPLICATION STARTUP
# --------------------------------------------------

@app.on_event("startup")
async def startup_event():

    print("=" * 55)
    print("NEXUS AI BACKEND STARTED")
    print("=" * 55)
    print(f"Application: {APP_NAME}")
    print(f"Version: {APP_VERSION}")
    print("API Status: ONLINE")
    print("=" * 55)


# --------------------------------------------------
# APPLICATION SHUTDOWN
# --------------------------------------------------

@app.on_event("shutdown")
async def shutdown_event():

    print("NEXUS AI Backend shutting down...")
