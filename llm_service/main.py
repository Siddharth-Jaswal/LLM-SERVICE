from fastapi import FastAPI
from llm_service.routes import health, chat
from llm_service.core.config import settings

app = FastAPI(title="LLM Gateway", description="Simple scalable FastAPI LLM Gateway")

app.include_router(health.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("llm_service.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
