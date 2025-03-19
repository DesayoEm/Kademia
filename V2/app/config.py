from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
load_dotenv()  # Make sure this loads variables from .env

class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    APP_NAME: str = "Kademia"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
config = Settings()

