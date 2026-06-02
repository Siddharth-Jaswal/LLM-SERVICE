from fastapi import FastAPI
from llm_service.routes import health, chat

app = FastAPI(title="LLM Gateway", description="Simple scalable FastAPI LLM Gateway")

app.include_router(health.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
