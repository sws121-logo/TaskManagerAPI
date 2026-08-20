from pydantic import BaseSettings, Field
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "TaskManagerAPI"
    DEBUG: bool = False
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    ENABLE_DOCS: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()