from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import EmailStr
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Kademia"
    ANONYMIZED_ID: str
    DEBUG: bool = False

    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379

    EXPORT_DIR: str

    AWS_ACCESS_KEY_ID :str
    AWS_SECRET_ACCESS_KEY :str
    AWS_DEFAULT_REGION :str
    AWS_BUCKET_NAME: str
    PROFILE_PICTURES_FOLDER: str


    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
config = Settings()


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    class Config:
        env_file = "../.env"
        env_prefix = "EMAIL_"

email_settings = EmailSettings()
