from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LCH_", env_file=".env", extra="ignore")

    env: str = "development"
    database_url: str = "postgresql+asyncpg://lch:lch@localhost:5432/lch_os"
    redis_url: str = "redis://localhost:6379/0"

    pbos_webhook_secret: str = "change-me"
    llm_provider: str = "openai"          # openai | anthropic | local
    llm_api_key: str = ""
    tts_provider: str = "elevenlabs"      # elevenlabs | azure | local
    tts_api_key: str = ""

    default_llm_model: str = "gpt-4o-mini"
    target_response_latency_ms: int = 2500

    compliance_strict: bool = True
    disclosure_interval_minutes: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()
