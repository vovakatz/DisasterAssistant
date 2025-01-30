from fastapi import APIRouter

from app.api.v1.endpoints import sample, assistant

api_router = APIRouter()
api_router.include_router(sample.router)
api_router.include_router(assistant.router)