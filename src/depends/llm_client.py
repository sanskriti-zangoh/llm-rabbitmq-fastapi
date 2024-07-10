from typing import List, AsyncGenerator
from contextlib import asynccontextmanager
import asyncio

from contextlib import asynccontextmanager
from api.schemas.llm import MessageRequestValidation, AnthropicConstant, MessageRequestOllama
from core.settings import ServiceCallerConfig
from exceptions.llm import ServiceError
from anthropic import AsyncAnthropic
from core.settings import load_settings, AnthropicSettings
from ollama import AsyncClient

from langchain_community.llms.ollama import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler    
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains.llm import LLMChain
from fastapi.responses import StreamingResponse
import anyio

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

class OllamaClient:
    def __init__(self):
        """
        Initialize Ollama service using langchain.
        """
        self.ollama = Ollama(base_url="http://ollama:11434", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    
    async def create_stream(self, messages: MessageRequestOllama, system: str,
                            temperature: float = settings.temperature,
                            model: AnthropicConstant.Model = settings.model) -> AsyncGenerator[str, None]:
        """
        Create stream message on Ollama.

        Args:
            messages (list): Messages to send.
            system (str): System description.
            max_tokens (int): Maximum tokens.
            temperature (float): Temperature.
            model (str): Model name.

        Returns:
            AsyncGenerator: Ollama streaming responses.
        """
        # self.ollama = Ollama(
        #     model=model,
        #     temperature=temperature,
        #     callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        #     system=system,
        #     base_url="http://ollama:11434"
        # )

        # return self.ollama.astream(input=messages.input)

        return self.ollama.astream(model=model, temperature=temperature, system=system, input=messages.input)



anthropic_client = AnthropicClient()
ollama_client = OllamaClient()