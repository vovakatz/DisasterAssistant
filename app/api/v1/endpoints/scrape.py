from fastapi import APIRouter, HTTPException
from starlette.responses import HTMLResponse

from app.models.scrape_response import ScrapeResponse
from app.services.scrape_service import ScrapeService
from app.utils.url import validate_url

router = APIRouter()

@router.get("/scrape", response_model=ScrapeResponse)
async def get_scrape(url: str):
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    service = ScrapeService()
    return await service.get_page_content(url)
