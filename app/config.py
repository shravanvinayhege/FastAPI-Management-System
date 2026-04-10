from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_name: str
    secret_key: str
    database_port: str
    database_username: str
    algorithm: str
    access_token_expire_minutes: int

    # Comma-separated list. Examples:
    # - "*" (allow all)
    # - "http://localhost:3000,https://myapp.com"
    cors_origins: Optional[str] = None

    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.cors_origins:
            return ["*"]
        raw = self.cors_origins.strip()
        if raw == "*":
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]


settings = Settings()