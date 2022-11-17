from pydantic import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    app_name: str = "Fido Jira"
    MAX_ASSIGN_VALUE: int = os.getenv('MAX_ASSIGN_VALUE', 5)


@lru_cache()
def get_settings():
    return Settings()


settings = Settings()
