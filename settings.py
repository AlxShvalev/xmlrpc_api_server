import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Base application settings class."""

    SERVER_HOST: str = os.getenv("SERVER_HOST", "localhost")
    SERVER_PORT: int = os.getenv("SERVER_PORT", 8080)

    DB_NAME: str = os.getenv("DB_NAME", "postgres")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST: str = os.getenv("DB_PORT", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    SESSION_LIFETIME: int = 60 * 30 # Seconds
    CHALLENGE_MIN_LENGTH: int = 30
    CHALLENGE_MAX_LENGTH: int = 60

    PUBLIC_KEY1: int = 28491
    PUBLIC_KEY2: int = 6007
    DH_SECRET_KEY: int = os.getenv("DH_SECRET_KEY", 221)

    @property
    def database_url(self) -> str:
        """Get DB connection url."""
        return (
            "postgresql+psycopg2://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
