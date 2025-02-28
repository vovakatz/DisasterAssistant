from fastapi import APIRouter

from app.pages import home, scrape

page_router = APIRouter()
page_router.include_router(home.router)
page_router.include_router(scrape.router)