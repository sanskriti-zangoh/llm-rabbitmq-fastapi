from fastapi import APIRouter, Depends

router = APIRouter(prefix="/llm", tags=["LLM"])

from depends.llm import LLMService
from api.schemas.llm import RequestValidation, RequestValidationOllama
from fastapi.responses import StreamingResponse
from rabbitmq.producer import RabbitMQProducer
from rabbitmq.producer_instance import get_producer


@router.post("/anthropic")
async def create_stream(body: RequestValidation) -> StreamingResponse:
    """
    Create stream message on LLM service.

    Args:
        body (RequestValidation): LLM request validation.

    Returns:
        StreamingResponse: LLM Message response.
    """
    return await LLMService.create_stream_anthropic(body=body)


@router.post("/ollama")
async def create_stream_ollama(body: RequestValidationOllama) -> StreamingResponse:
    """
    Create stream message on LLM service.

    Args:
        body (RequestValidation): LLM request validation.

    Returns:
        StreamingResponse: LLM Message response.
    """
    return await LLMService.create_stream_ollama(body=body)   

@router.post("/ollama/mq")
async def create_stream_ollama(body: RequestValidationOllama, producer: RabbitMQProducer = Depends(get_producer)) -> StreamingResponse:
    """
    Create stream message on LLM service.

    Args:
        body (RequestValidation): LLM request validation.

    Returns:
        StreamingResponse: LLM Message response.
    """
    # return await LLMService.create_stream_ollama(body=body)   

    try:
        await producer.publish("ollama", await LLMService.create_stream_ollama(body=body))
        return "OK"
    except Exception as e:
        return str(e)