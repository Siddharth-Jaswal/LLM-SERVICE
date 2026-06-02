from fastapi import APIRouter, Depends, UploadFile, Form
from fastapi.responses import StreamingResponse
from llm_service.schemas.request import ChatRequest
from llm_service.schemas.response import ChatResponse
from llm_service.services.chat_service import ChatService
from llm_service.providers.lmstudio import LMStudioProvider
from typing import Dict, Any

router = APIRouter()

# Dependency injection for the provider
def get_provider():
    return LMStudioProvider()

# Dependency injection for the service
def get_chat_service(provider = Depends(get_provider)):
    return ChatService(provider)

@router.get("/models")
async def get_models(service: ChatService = Depends(get_chat_service)) -> Dict[str, Any]:
    return await service.get_models()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest, service: ChatService = Depends(get_chat_service)):
    result = await service.process_chat(request.message, request.stream)
    if request.stream:
        return StreamingResponse(result, media_type="text/plain")
    return ChatResponse(response=result)

@router.post("/vision")
async def vision_endpoint(
    message: str = Form(...),
    stream: bool = Form(False),
    image: UploadFile = Form(...),
    service: ChatService = Depends(get_chat_service)
):
    image_bytes = await image.read()
    result = await service.process_vision(message, image_bytes, stream)
    if stream:
        return StreamingResponse(result, media_type="text/plain")
    return ChatResponse(response=result)
