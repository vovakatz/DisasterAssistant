from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.pages.router import page_router

app = FastAPI(title="FastAPI Service", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")
app.include_router(page_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get('/favicon.ico')
async def favicon():
    file_name = "app/static/favicon.ico"
    return FileResponse(file_name)