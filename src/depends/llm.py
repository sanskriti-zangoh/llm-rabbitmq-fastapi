
from fastapi.responses import StreamingResponse

from api.schemas.llm import RequestValidation
from core.settings import  BusinessLogicConfig
from exceptions.llm import ServiceError

from depends.llm_client import anthropic_client

class LLMService:

    @staticmethod
    async def create_stream(body: RequestValidation) -> StreamingResponse:
        """
        Create stream message on anthropic.

        Args:
            body (RequestValidation): Anthropic request validation.

        Returns:
            StreamingResponse: Anthropic Message response.
        """
        system = BusinessLogicConfig.get_system_message(system=body.system)

        try:
            return StreamingResponse(
                content=anthropic_client.create_stream(messages=body.messages, system=system,
                                                       model=body.model,
                                                       max_tokens=body.max_tokens,
                                                       temperature=body.temperature),
                media_type="text/plain")
        except Exception as e:
            raise ServiceError(f"Failed to create stream message on anthropic: {str(e)}")