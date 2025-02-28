from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter

from app.pages import templates

router = APIRouter()

@router.get("/scrapeme", response_class=HTMLResponse)
async def scrape(request: Request):
    return templates.TemplateResponse("scrape.html", {"request": request})