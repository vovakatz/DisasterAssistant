from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter

from app.pages import templates

router = APIRouter()

@router.get("/scrape", response_class=HTMLResponse)
async def scrape(request: Request):
    return templates.TemplateResponse(request, "scrape.html")