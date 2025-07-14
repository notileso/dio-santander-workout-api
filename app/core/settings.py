from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

__all__ = ["Settings", "settings"]


class Settings(BaseSettings):
    DB_URL: str = Field(default="postgresql+asyncpg://workout:workout@localhost/workout")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings() # type: ignore