from fastapi import APIRouter

from app.api.v1.endpoints import sample, assistant, scrape

api_router = APIRouter()
api_router.include_router(sample.router)
api_router.include_router(assistant.router)
api_router.include_router(scrape.router)
