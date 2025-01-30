import os

from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
    project="proj_gLqeI29UOxol45PyQiFT5jAN",
)