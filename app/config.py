from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings loaded from the environment and .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PayLinkHub"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    core_base_url: str = "https://dummyjson.com/users"
    pagos_base_url: str = "https://dummyjson.com/carts/user"
    core_timeout_seconds: float = 10.0
    pagos_timeout_seconds: float = 10.0


@lru_cache
def get_settings() -> Settings:
    return Settings()
