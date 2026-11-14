from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Image Search"
    database_url: str
    redis_url: str
    gemini_api_key: str
    gemini_model: str = "gemini-3.7-flash"
    max_image_size_mb: int = 10
    max_image_pixels: int = 25_000_000
    vector_dim: int = 512
    top_k: int = 20
    rerank_k: int = 8
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
settings = get_settings()
