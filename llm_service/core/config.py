from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LMSTUDIO_URL: str = "http://localhost:1234"
    MODEL: str = "qwen3-vl-8b-instruct"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
