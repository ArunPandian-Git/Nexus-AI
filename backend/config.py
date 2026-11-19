%%writefile /content/backend/config.py

from pathlib import Path
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):

    app_name: str = "NEXUS AI"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    api_prefix: str = "/api/v1"

    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4.1-mini"

    database_url: str = "sqlite:///./nexus.db"

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: SecretStr | None = None

    secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
