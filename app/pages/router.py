from fastapi import APIRouter

from app.pages import home

page_router = APIRouter()
page_router.include_router(home.router)