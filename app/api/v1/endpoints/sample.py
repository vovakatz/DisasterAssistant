from fastapi import APIRouter

from app.services.sample_service import SampleService
from app.models.sample import SampleResponse

router = APIRouter()

@router.get("/sample", response_model=SampleResponse)
async def get_sample():
    service = SampleService()
    return service.get_sample_data()