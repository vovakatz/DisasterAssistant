from pydantic import BaseModel

class AssistantResponse(BaseModel):
    thread_id: str
    message: str