import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY', '')
    PROJECT_ID: str = "proj_gLqeI29UOxol45PyQiFT5jAN"
    ASSISTANT_ID: str = "asst_sh3cHFY9moqlcjt8wvW5ZqMa"
    VECTOR_STORE_ID: str = 'vs_9sVchxI3emlMflZKdohp7aJ5'

    class Config:
        case_sensitive = True


settings = Settings()