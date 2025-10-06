from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    google_api_key: str
    port: int = 5000
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings():
    return Settings(
        google_api_key=os.getenv("GOOGLE_API_KEY", ""),
        port=int(os.getenv("PORT", "5000"))
    )
