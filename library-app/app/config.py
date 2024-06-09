import os
from typing import List

from pydantic import AnyHttpUrl
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DEVELOPER_MODE = True
    SECRET_KEY: str = (
        "8IPmBc32oGbXddLeXA-uu0w5zK_cNj1ayhg7j4xCK6mWGk5Ry_mvkfZYwjFkDLCU4kEqs-yHtiQENsBzqFRJgQ"
    )

    # PostgreSQL
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE", "library")
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    )
    SQLALCHEMY_ECHO: bool = False

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_TIME: int = 10000

    # REDIS
    REDIS_URL: str = "redis://localhost:6379/0"

    # CELERY
    CELERY_BROKER: str = os.environ.get(
        "CELERY_BROKER", "redis://127.0.0.1:6379/0"
    )
    CELERY_BACKEND: str = os.environ.get(
        "CELERY_BACKEND", "redis://127.0.0.1:6379/0"
    )

    # BOOK
    BORROW_TIME_IN_DAY: int = 7

    # EMAIL
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM = os.environ.get("MAIL_FROM")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME")
    TEMPLATE_FOLDER = os.environ.get("TEMPLATE_FOLDER")

    TIMEZONE: str = "Europe/Istanbul"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []


settings = Settings()
