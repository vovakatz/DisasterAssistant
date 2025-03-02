import os
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.router import api_router
from app.auth.middleware import AdminRouteMiddleware
from app.auth.routes import auth_router
from app.core.config import settings
from app.pages.router import page_router

app = FastAPI(title="FastAPI Service", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")
app.include_router(page_router)
app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get('/favicon.ico')
async def favicon():
    file_name = "app/static/favicon.ico"
    return FileResponse(file_name)


# Add the middleware to the application
app.add_middleware(AdminRouteMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)