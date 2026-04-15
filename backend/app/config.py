from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://fayni_user:change-me-demo-password@db:5432/fayni_db"
    secret_key: str = "change-this-secret-before-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    class Config:
        env_file = ".env"


settings = Settings()
