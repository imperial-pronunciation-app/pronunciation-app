from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    USER_MANAGER_SECRET: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    BUCKET_NAME: str
    MODEL_API_URL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore[call-arg]