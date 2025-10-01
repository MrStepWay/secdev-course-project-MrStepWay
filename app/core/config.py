from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс для управления настройками. Читает переменные из .env файла
    """
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
