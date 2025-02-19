import io
import time

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

            self.add_file_to_assistant(result.markdown, "sample_file_1.md", "asst_sh3cHFY9moqlcjt8wvW5ZqMa")
            return ScrapeResponse(content=result.markdown)

    def add_file_to_assistant(self, file_content, filename, assistant_id):
        file_buffer = io.BytesIO(file_content.encode() if isinstance(file_content, str) else file_content)

        # Upload the file content to OpenAI
        file_response = client.files.create(
            file=(filename, file_buffer),
            purpose="assistants"
        )
        file_id = file_response.id

        vector_store_id = 'vs_9sVchxI3emlMflZKdohp7aJ5'

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