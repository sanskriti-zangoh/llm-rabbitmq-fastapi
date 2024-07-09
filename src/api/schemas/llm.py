from pydantic import BaseModel, Field, model_validator
from typing import Iterable, Annotated
from enum import Enum
from os import PathLike
import json

class StrEnum(str, Enum):
    pass

class AnthropicConstant:
    class ImageBlock:
        class MediaType(StrEnum):
            JPEG = "image/jpeg"
            PNG = "image/png"
            GIF = "image/gif"
            WEBP = "image/webp"

        class DataFormat(StrEnum):
            BASE64 = "base64"

        class Type(StrEnum):
            IMAGE = "image"

    class TextBlock:
        class Type(StrEnum):
            TEXT = "text"

    class Role(StrEnum):
        USER = "user"
        ASSISTANT = "assistant"

    class StopReason(StrEnum):
        END_TURN = "end_turn"
        MAX_TOKENS = "max_tokens"
        STOP_SEQUENCE = "stop_sequence"

    class Type(StrEnum):
        MESSAGE = "message"

    class Model(StrEnum):
        CLAUDE_3_OPUS_20240229 = "claude-3-opus-20240229"
        CLAUDE_3_SONNET_20240229 = "claude-3-sonnet-20240229"
        CLAUDE_3_HAIKU_20240307 = "claude-3-haiku-20240307"
        CLAUDE_2_1 = "claude-2.1"
        CLAUDE_2_0 = "claude-2.0"
        CLAUDE_INSTANT_1_2 = "claude-instant-1.2"


class ImageSource(BaseModel):
    media_type: AnthropicConstant.ImageBlock.MediaType
    type: AnthropicConstant.ImageBlock.DataFormat
    data: Annotated[str | PathLike, dict(format=AnthropicConstant.ImageBlock.DataFormat.BASE64)]

class TextBlock(BaseModel):
    text: str
    type: AnthropicConstant.TextBlock.Type

class ImageBlock(BaseModel):
    source: ImageSource
    type: AnthropicConstant.ImageBlock.Type

class MessageRequestValidation(BaseModel):
    content: str | Iterable[TextBlock | ImageBlock]
    role: AnthropicConstant.Role

class RequestValidation(BaseModel):
    messages: list[MessageRequestValidation]
    system: str | None = Field("You are a personal AI assistant",
                               title='System', description='The system name.')
    max_tokens: int | None = Field(1024, ge=1, title='Max Tokens',
                                   description='The maximum number of tokens to generate.')
    temperature: float | None = Field(0.8, title='Temperature', gt=0.0, le=1.0,
                                      description='The sampling temperature.')
    model: AnthropicConstant.Model | None = Field(AnthropicConstant.Model.CLAUDE_3_OPUS_20240229,
                                                  title='Model', description='The model name.')

    @model_validator(mode="before")
    @classmethod
    def to_py_dict(cls, data):
        return json.loads(data)