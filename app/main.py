from fastapi import FastAPI
from app.api.v1.endpoints import sample

app = FastAPI(title="FastAPI Service", version="1.0.0")

app.include_router(sample.router, prefix="/api/v1")