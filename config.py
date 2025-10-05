from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env")


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_POST: int
    POSTGRES_HOST: str
    CELERY_BROKER: str
    CELERY_RESULT: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @property
    def db_async_credentials(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_POST}/{self.POSTGRES_DB}"
        )


settings = Settings()


