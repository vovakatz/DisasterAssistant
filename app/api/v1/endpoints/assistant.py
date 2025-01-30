from fastapi import APIRouter

from app.models.assistant_request import QuestionRequest
from app.models.assistant_response import AssistantResponse
from app.services.assistant_service import AssistantService

router = APIRouter()

@router.post("/assistant", response_model=AssistantResponse)
async def get_sample(r: QuestionRequest):
    service = AssistantService()
    return service.get_assistant_response(r.question, r.thread_id)