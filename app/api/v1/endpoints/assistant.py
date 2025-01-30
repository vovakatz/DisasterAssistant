from fastapi import APIRouter

from app.models.assistant_response import AssistantResponse
from app.services.assistant_service import AssistantService

router = APIRouter()

@router.get("/assistant", response_model=AssistantResponse)
async def get_sample(q:str, t:str|None = None):
    service = AssistantService()
    return service.get_assistant_response(q,t)