import io
import time

from app.core.config import settings
from app.models.scrape_response import ScrapeResponse
from crawl4ai import *

from app.services import client


class ScrapeService:
    async def get_page_content(self, url: str):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
            )

            if not result.success:
               raise RuntimeError("Crawler was not successful.")

            if len(result.markdown) == 0:
                raise ValueError("Crawler returned empty content")

            return ScrapeResponse(content=result.markdown)


    def add_file_to_assistant(self, file_content, filename):
        file_buffer = io.BytesIO(file_content.encode() if isinstance(file_content, str) else file_content)

        # Upload the file content to OpenAI
        file_response = client.files.create(
            file=(filename, file_buffer),
            purpose="assistants"
        )
        file_id = file_response.id

        vector_store_id = settings.VECTOR_STORE_ID

        # Add the file to the vector store
        batch_response = client.beta.vector_stores.file_batches.create(
            vector_store_id=vector_store_id,
            file_ids=[file_id]
        )
        batch_id = batch_response.id

        # Check the status of the batch
        while True:
            batch_status = client.beta.vector_stores.file_batches.retrieve(
                vector_store_id=vector_store_id,
                batch_id=batch_id
            )
            status = batch_status.status
            if status in ['completed', 'failed']:
                break
            time.sleep(1)

        if status != 'completed':
            raise RuntimeError("Failed to upload file to vector store.")