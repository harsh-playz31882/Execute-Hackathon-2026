from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # NOTE: For hackathon/local use only.
    # Override these via environment variables or a .env file in real deployments.
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()


__all__ = ["settings"]
