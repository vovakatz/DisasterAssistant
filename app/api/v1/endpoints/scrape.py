from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException

from app.models.scrap_request import ScrapRequest
from app.models.scrape_response import ScrapeResponse
from app.services.scrape_service import ScrapeService
from app.utils.url import validate_url

router = APIRouter()


@router.get("/scrape", response_model=ScrapeResponse)
async def get_scrape(url: str):
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    service = ScrapeService()
    try:
        return await service.get_page_content(url)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Exceptions occurred while processing the request")


@router.post("/scrape")
async def save_scrap(scrap_request: ScrapRequest):
    if not validate_url(scrap_request.url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    service = ScrapeService()
    try:
        filename = urlparse(scrap_request.url).netloc + ".md"
        service.add_file_to_assistant(scrap_request.content, filename)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Exceptions occurred while processing the request")
