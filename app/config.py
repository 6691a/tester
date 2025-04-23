from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file

_BASE_DIR: Path = Path(__file__).parent
_ROOT_DIR: Path = _BASE_DIR.parent


class Settings(BaseSettings):
    BASE_DIR: Path = _BASE_DIR
    ROOT_DIR: Path = _ROOT_DIR

    # Ollama settings
    OLLAMA_BASE_URL: str
    OLLAMA_MODEL: str
    OLLAMA_TEMPERATURE: float = 0.0

    # Vector DB settings
    VECTOR_DB_PATH: str

    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    DATABASE_URL: str = ""

    DEBUG: bool = True

    # API settings
    API_PREFIX: str = "/api/v1"
    model_config = SettingsConfigDict(
        env_file=str(_ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.DATABASE_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
