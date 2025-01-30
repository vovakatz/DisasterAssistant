from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter

from app.pages import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})