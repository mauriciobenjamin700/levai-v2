"""Application settings module using Pydantic for environment variable management."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or a .env file.

    Attributes:
        DB_URL (str): Database connection URL.
        DB_USER (str): Database user.
        DB_PASSWORD (str): Database password.
        DB_HOST (str): Database host.
        DB_PORT (str): Database port.
        DB_NAME (str): Database name.
        TEST_DB_URL (str): Test database connection URL.

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    DB_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    TEST_DB_URL: str
