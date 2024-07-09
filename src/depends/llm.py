from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from typing import List

from api.schemas.llm import RequestValidation, MessageRequestValidation, AnthropicConstant
from core.settings import ServiceCallerConfig, BusinessLogicConfig
from exceptions.llm import ServiceError
from anthropic import AsyncAnthropic

class AnthropicClient:
    def __init__(self):
        """
        Initialize Anthropic service.
        """
        anthropic_api_key = ServiceCallerConfig.Anthropic.API_KEY
        if not anthropic_api_key:
            raise ServiceError("Anthropic API key is not set.")

        self.anthropic = AsyncAnthropic(api_key=anthropic_api_key)

    async def create_stream(self, messages: List[MessageRequestValidation], system: str,
                            max_tokens: int = ServiceCallerConfig.Anthropic.MAX_TOKEN,
                            temperature: float = ServiceCallerConfig.Anthropic.TEMPERATURE,
                            model: AnthropicConstant.Model = ServiceCallerConfig.Anthropic.MODEL):
        """
        Create stream message on anthropic.

        Args:
            messages (list): Messages to send.
            system (str): System description.
            max_tokens (int): Maximum tokens.
            temperature (float): Temperature.
            model (str): Model name.

        Returns:
            MessageResponseValidation: Anthropic Message response.
        """
        async with self.anthropic.messages.stream(model=model, max_tokens=max_tokens, temperature=temperature,
                                                  system=system, messages=messages) as stream:
            async for text in stream.text_stream:
                yield text


anthropic_client = AnthropicClient()

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