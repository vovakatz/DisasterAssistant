from pydantic import BaseModel

class ScrapeResponse(BaseModel):
    content: str
