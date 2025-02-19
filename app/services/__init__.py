import os

from fastapi import FastAPI
from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    project=settings.PROJECT_ID,
)