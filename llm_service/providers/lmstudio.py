import json
import httpx
from typing import Dict, Any, Union, AsyncGenerator
from llm_service.providers.base import BaseProvider
from llm_service.core.config import settings

class LMStudioProvider(BaseProvider):
    def __init__(self):
        self.base_url = f"{settings.LMSTUDIO_URL}/v1"
        self.model = settings.MODEL

    async def _stream_generator(self, response: httpx.Response) -> AsyncGenerator[str, None]:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data.get("choices", [{}])[0].get("delta", {})
                    if "content" in delta:
                        yield delta["content"]
                except json.JSONDecodeError:
                    continue

    async def _stream_chat(self, payload: dict) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", f"{self.base_url}/chat/completions", json=payload, timeout=60.0) as response:
                response.raise_for_status()
                async for chunk in self._stream_generator(response):
                    yield chunk

    async def _stream_vision(self, payload: dict) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", f"{self.base_url}/chat/completions", json=payload, timeout=120.0) as response:
                response.raise_for_status()
                async for chunk in self._stream_generator(response):
                    yield chunk

    async def chat(self, message: str, stream: bool = False) -> Union[str, AsyncGenerator[str, None]]:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "stream": stream
        }
        
        if stream:
            return self._stream_chat(payload)
            
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/chat/completions", json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def vision(self, message: str, image_base64: str, stream: bool = False) -> Union[str, AsyncGenerator[str, None]]:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "stream": stream
        }
        
        if stream:
            return self._stream_vision(payload)
            
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/chat/completions", json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def models(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/models", timeout=10.0)
            response.raise_for_status()
            return response.json()
