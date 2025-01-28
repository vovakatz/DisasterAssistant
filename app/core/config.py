import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Service"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"

settings = Settings()