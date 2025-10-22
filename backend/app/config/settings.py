from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_version: str = "0.1.0"
    env: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    # Кэширование исключает повторное чтение переменных окружения
    return Settings()


