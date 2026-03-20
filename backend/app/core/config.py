from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Retail Arbitrage Deal Finder API"
    environment: str = "dev"
    debug: bool = True
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/retail_arbitrage"
    redis_url: str = "redis://localhost:6379/0"
    request_timeout_seconds: int = 20
    adapter_rate_limit_per_minute: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
