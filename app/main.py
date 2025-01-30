from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.pages.router import page_router

app = FastAPI(title="FastAPI Service", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")
app.include_router(page_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")