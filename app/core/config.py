import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY', '')
    PROJECT_ID: str = "proj_gLqeI29UOxol45PyQiFT5jAN"
    ASSISTANT_ID: str = "asst_sh3cHFY9moqlcjt8wvW5ZqMa"
    VECTOR_STORE_ID: str = "vs_9sVchxI3emlMflZKdohp7aJ5"
    GOOGLE_CLIENT_ID: str = "55708612763-002smoul84affv2kapcge6ot64c942sm.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET: str = os.environ.get('GOOGLE_CLIENT_SECRET', '')
    SECRET_KEY: str = "some_random_key"
    # Allowed Google emails or domains
    # Example: ["user@example.com", "admin@company.com"] or ["@company.com"]
    ALLOWED_EMAILS: [str] = os.environ.get("ALLOWED_EMAILS", "vovakats@gmail.com,jvmandel@gmail.com").split(",")
    ALLOWED_DOMAINS: [str] = os.environ.get("ALLOWED_DOMAINS", "").split(",")

    class Config:
        case_sensitive = True

settings = Settings()