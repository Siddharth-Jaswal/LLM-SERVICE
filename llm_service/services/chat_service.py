import base64
from typing import Dict, Any, Union, AsyncGenerator
from llm_service.providers.base import BaseProvider

class ChatService:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    async def process_chat(self, message: str, stream: bool = False) -> Union[str, AsyncGenerator[str, None]]:
        return await self.provider.chat(message, stream)

    async def process_vision(self, message: str, image_bytes: bytes, stream: bool = False) -> Union[str, AsyncGenerator[str, None]]:
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        return await self.provider.vision(message, image_base64, stream)

    async def get_models(self) -> Dict[str, Any]:
        return await self.provider.models()
