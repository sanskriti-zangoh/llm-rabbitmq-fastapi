from typing import List

from api.schemas.llm import MessageRequestValidation, AnthropicConstant
from core.settings import ServiceCallerConfig
from exceptions.llm import ServiceError
from anthropic import AsyncAnthropic
from core.settings import load_settings, AnthropicSettings


settings: AnthropicSettings = load_settings("AnthropicSettings")

class AnthropicClient:
    def __init__(self):
        """
        Initialize Anthropic service.
        """
        anthropic_api_key = settings.api_key
        if not anthropic_api_key:
            raise ServiceError("Anthropic API key is not set.")

        self.anthropic = AsyncAnthropic(api_key=anthropic_api_key)

    async def create_stream(self, messages: List[MessageRequestValidation], system: str,
                            max_tokens: int = settings.max_tokens,
                            temperature: float = settings.temperature,
                            model: AnthropicConstant.Model = settings.model):
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