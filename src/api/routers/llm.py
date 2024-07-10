from fastapi import APIRouter

router = APIRouter(prefix="/llm", tags=["LLM"])

from depends.llm import LLMService
from api.schemas.llm import RequestValidation
from fastapi.responses import StreamingResponse


@router.post("/stream")
async def create_stream(body: RequestValidation) -> StreamingResponse:
    """
    Create stream message on LLM service.

    Args:
        body (RequestValidation): LLM request validation.

    Returns:
        StreamingResponse: LLM Message response.
    """
    return await LLMService.create_stream(body=body)