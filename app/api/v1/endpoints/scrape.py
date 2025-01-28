from fastapi import APIRouter

from app.models.scrape import ScrapeResponse
from app.services.scrape_service import ScrapeService

router = APIRouter()

@router.get("/scrape", response_model=ScrapeResponse)
async def get_scrape(url: str):
    service = ScrapeService()
    return await service.get_page_content(url)