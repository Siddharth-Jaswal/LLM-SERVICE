from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LMSTUDIO_URL: str = "http://localhost:1234"
    MODEL: str = "qwen3-vl-8b-instruct"

    class Config:
        env_file = ".env"

settings = Settings()
