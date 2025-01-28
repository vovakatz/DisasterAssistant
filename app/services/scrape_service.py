from app.models.scrape import ScrapeResponse
from crawl4ai import *

class ScrapeService:
    async def get_page_content(self, url: str):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
            )
            return ScrapeResponse(content=result.markdown)


