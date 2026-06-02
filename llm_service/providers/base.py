from abc import ABC, abstractmethod
from typing import Dict, Any, Union, AsyncGenerator

class BaseProvider(ABC):
    @abstractmethod
    async def chat(self, message: str, stream: bool = False) -> Union[str, AsyncGenerator[str, None]]:
        """Process a text-only chat message."""
        pass

    @abstractmethod
    async def vision(self, message: str, image_base64: str, stream: bool = False) -> Union[str, AsyncGenerator[str, None]]:
        """Process a text message along with an image."""
        pass

    @abstractmethod
    async def models(self) -> Dict[str, Any]:
        """Return available models."""
        pass
